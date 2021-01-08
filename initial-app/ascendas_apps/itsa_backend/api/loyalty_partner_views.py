from __future__ import absolute_import
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from datetime import datetime
from django.views.decorators.cache import cache_page
from django.conf import settings 
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core import serializers

from utils.LoyaltyPartnerChecker import LoyaltyPartnerChecker

import boto3
import tempfile
import shutil
import json
import random
import string
import requests
import csv
from datetime import datetime

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
SQS_URL = ["https://sqs.ap-southeast-1.amazonaws.com/731706226892/", "-poll.fifo"]

## TODO: CHANGE TO LOYALTY PARTNER EB ENDPOINT
LOYALTY_PARTNER_ENDPOINT = "http://localhost:5000"
# LOYALTY_PARTNER_ENDPOINT = "loyalty-partner-backend-dev.ap-southeast-1.elasticbeanstalk.com"
try:
    session = boto3.Session(profile_name="ITSA")
    s3 = session.client("s3")
    sns = session.client("sns", region_name="ap-southeast-1")
    sqs = session.client('sqs', region_name="ap-southeast-1")
except:
    s3 = boto3.client("s3")
    sns = boto3.client("sns", region_name="ap-southeast-1")
    sqs = boto3.client('sqs', region_name="ap-southeast-1")

"""
DATA VALIDATION
"""
def generateUniqueNumber() -> str:
    result = ""
    num_of_parts = random.randrange(3, 6)
    alpha_digits = string.ascii_letters + string.digits
    for _ in range(num_of_parts):
        for __ in range(5):
            result += alpha_digits[random.randrange(len(alpha_digits))]

    return (result)

@csrf_exempt
def loyalty_program_handback_file_submission(request):
    """
    Frontend Uploads Handback File --> Lambda receives handback file --> Lambda sends handback file w bucket and key to this endpoint
    Triggered by Lambda function
    Lambda function will send 
    1. bucket
    2. key 
    as params in GET request
    """
    if request.method == "GET":
        bucket = request.GET.get("bucket", False)
        key = request.GET.get("key", False)
        if bucket and key:
            try:
                session = boto3.Session(profile_name="ITSA")
                s3 = session.client("s3")
            except:
                s3 = boto3.client("s3")

            dirpath = tempfile.mkdtemp()
            filename = dirpath + key

            try:
                s3.download_file(Bucket=bucket, Key=key, Filename=filename)
            except:
                return HttpResponse("File does not exist", status=404)

            try:
                with open(filename) as fp:
                    i = 0
                    for row in fp:
                        if i == 0:
                            i += 1
                            continue
                        line = row.split(",")
                        # Validate row by row --> If have errors, collate errors and send back response
                        # If no error --> Add to databas
                        date = line[0]
                        amount = line[1]
                        transaction_id = line[2]
                        outcome_code = line[3].strip().strip("'")
                        try:
                            target_transaction = Transaction.objects.get(transactionId=str(transaction_id))
                            Transaction.objects.filter(transactionId=str(transaction_id)).update(outcomeCode=outcome_code)

                            membershipNumber = target_transaction.membershipNumber
                            target_membership = Membership.objects.get(membershipNumber=membershipNumber)
                            userId = target_membership.userId
                            target_user = User.objects.get(userId=int(userId.userId))
                            new_point_balance = int(target_user.pointBalance) - int(amount)
                            print (new_point_balance)
                            if new_point_balance < 0:
                                new_point_balance = target_user.pointBalance
                            target_user = User.objects.get(userId=int(userId.userId))
                            target_user.pointBalance = str(new_point_balance)
                            target_user.save()

                            outcome_code = outcome_code.strip("'").strip("`").strip("`")

                            unique_message_id = str(target_transaction.membershipNumber) + str(target_transaction.transactionId) + str(outcome_code) + str(amount)
                            
                            ## SQS time
                            sqs_body = {
                                'memberId': str(target_transaction.membershipNumber), 
                                'transactionCode': str(target_transaction.transactionId),
                                'outcomeCode': str(outcome_code),
                                "amount": str(amount)
                            }

                            sqs_body = json.dumps(sqs_body)
                            sqs_response = sqs.send_message(
                                QueueUrl=SQS_URL[0] + target_transaction.partnerCode.lower() + SQS_URL[1],
                                MessageAttributes={
                                    'memberId': {
                                        'DataType': "String",
                                        'StringValue': target_transaction.membershipNumber
                                    },
                                    'transactionCode': {
                                        'DataType': "String",
                                        "StringValue": str(target_transaction.transactionId)
                                    },
                                    'outcomeCode': {
                                        'DataType': "String",
                                        "StringValue": outcome_code
                                    },
                                    "amount": {
                                        "DataType": "String",
                                        "StringValue": amount
                                    }

                                },
                                MessageBody=sqs_body,
                                MessageDeduplicationId=unique_message_id,
                                MessageGroupId='string'
                            )
                            sqs_message_id = sqs_response["MessageId"]

                        except Exception as e:
                            ## TODO: write the errornous lines and return to loyalty partner
                            print (e)
            
            except Exception as e:
                print (e)

            shutil.rmtree(dirpath)

            return JsonResponse("Completed", safe=False)
        
        return HttpResponse("Invalid attributes in url. Please check", status=404)

    return HttpResponse("Invalid method", status=401)

@csrf_exempt
def validate_membership_id(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        member_id = data.get("membershipNumber", False)
        loyalty_partner_name = data.get("loyaltyPartnerName", False)

        if member_id and loyalty_partner_name:
            checker = LoyaltyPartnerChecker(loyalty_partner_name, member_id)
            if checker.verify_member_id():
                membershipData = Membership.objects.get(membershipNumber__exact = member_id)
                serializer = MembershipSerializer(membershipData)
                return JsonResponse(serializer.data, status=200)

        return JsonResponse({"result": "invalid"}, status=400)


@csrf_exempt
def loyaltyprogram_new_accrual(request):
    """
    This gets called from Bank's frontend to insert a new transaction into the DB

    1. User cr8s accural request
    2. Bank send accural request to Ascenda Middleware
    3. Asecnda Middleware stores transactions as "PENDING"
    4. AScenda Middle compiles batch file daily and sends to Loyalty Partner
    """
    if request.method == "POST":
        data = JSONParser().parse(request)
        loyalty_program_name = data.get("loyalty_program_name", False) ## gojet points
        member_id = data.get("member_id", False) ## 2153642985
        first_name = data.get("first_name", False)# michael
        last_name = data.get("last_name", False) ## jackson
        transfer_date = data.get("transfer_date", False) ## 160398214112
        amount = data.get("amount", False) ## 900
        bank_partner_code = data.get("bank_code", False) ## testcode
        misc = data.get("misc", "") ## This is a message
        
        if (
            loyalty_program_name 
            and member_id 
            and first_name 
            and last_name 
            and transfer_date 
            and amount 
            and bank_partner_code
        ):            
            reference_number = datetime.now().strftime("%Y%m%dT%H%M%S%f")
            try:
                new_transaction = Transaction(
                    referenceNumber=reference_number,
                    membershipNumber=member_id,
                    partnerCode=bank_partner_code,
                    transactionDate=transfer_date,
                    transferAmount=amount,
                    additionalInfo=misc,
                    outcomeCode="PENDING",
                    loyaltyProgramId=loyalty_program_name,
                )
                new_transaction.save()
                
                ## SQS time
                sqs_body = {
                    'memberId': str(member_id), 
                    'transactionCode': str(new_transaction.transactionId),
                    'outcomeCode': "PENDING",
                    "amount": str(amount)
                }
                sqs_body = json.dumps(sqs_body)
                sqs_response = sqs.send_message(
                    QueueUrl=SQS_URL[0] + bank_partner_code.lower() + SQS_URL[1],
                    MessageAttributes={
                        'memberId': {
                            'DataType': "String",
                            'StringValue': str(member_id)
                        },
                        'transactionCode': {
                            'DataType': "String",
                            "StringValue": str(new_transaction.transactionId)
                        },
                        'outcomeCode': {
                            'DataType': "String",
                            "StringValue": "PENDING"
                        },
                        "amount": {
                            "DataType": "String",
                            "StringValue": str(amount)
                        }

                    },
                    MessageBody=sqs_body,
                    MessageDeduplicationId='string',
                    MessageGroupId='string'
                )
                sqs_message_id = sqs_response["MessageId"]

                return JsonResponse({"result": "success", "reference_number": new_transaction.transactionId}, status=200)

            except Exception as e:
                print (e)
                return JsonResponse({"result": "Invalid Payload"}, status=401)

        return JsonResponse({"result": "Missing Key"}, status=401)

    return JsonResponse({"result": "Invalid method"}, status=401)


@csrf_exempt
def generateBatchFile(request):
    """
    This gets called by the Lambda Function

    1. Lambda function gets triggered by CloudWatch daily
    2. Calls this endpoint and compiles file
    3. Sends file to loyaltyparter via self-signed url
    """
    temp_dir = tempfile.mkdtemp()
    try:
        if request.method == "POST":
            date = request.POST.get("date", False) ## 20200802
            if date:
                partnerCode = ""
                filename = f"{datetime.now().strftime('%Y%m%d')}.csv"
                filepath = f"{temp_dir}/{filename}"
                with open(f"{temp_dir}/{filename}", "w+") as fp:
                    csvWriter = csv.writer(fp)
                    all_transactions = Transaction.objects.all()
                    count = 1
                    row = [
                        "index", 
                        "Member ID",
                        "Member first name",
                        "Member last name",
                        "Transfer date",
                        "Amount",
                        "Reference number",
                        "Partner Code",
                        "Outcome code",
                    ]
                    csvWriter.writerow(row)
                    for trans in all_transactions:
                        if "".join(trans.transactionDate.split("-")) == date:
                            target_membership = Membership.objects.get(membershipNumber=trans.membershipNumber)
                            target_membership.userId.firstName

                            row = [
                                count, 
                                trans.membershipNumber,
                                target_membership.userId.firstName,
                                target_membership.userId.lastName,
                                trans.transactionDate,
                                trans.transferAmount,
                                trans.transactionId,
                                trans.partnerCode,
                                "\'" + trans.outcomeCode,
                            ]

                            csvWriter.writerow(row)
                            count += 1
                            partnerCode = trans.partnerCode

                s3.upload_file(filepath, "loyalty-partner-batch-files", f"{partnerCode}_{filename}")

                presignedUrl = s3.generate_presigned_url('get_object', Params={
                    'Bucket': "loyalty-partner-batch-files",
                    'Key': f"{partnerCode}_{filename}"
                }
                ,ExpiresIn=3600)
                
                sns.publish(
                    TopicArn="arn:aws:sns:ap-southeast-1:731706226892:topic_name", 
                    Message= presignedUrl, 
                    Subject=f"New Accrual Request: {partnerCode}_{filename}",
                )
            else:
                return HttpResponse("please give a date", 203)
    except Exception as e:
        print (e)

    finally:
        shutil.rmtree(temp_dir)

    return HttpResponse("success", 200) 

@csrf_exempt 
def test_sherman(request):
    try:
        if request.method == "GET":
            transaction_id = "300"
            outcome_code = "0000"
            amount = "69"

            target_transaction = Transaction.objects.get(transactionId=transaction_id)
            Transaction.objects.filter(transactionId=transaction_id).update(outcomeCode=outcome_code)

            membershipNumber = target_transaction.membershipNumber
            target_membership = Membership.objects.get(membershipNumber=membershipNumber)
            userId = target_membership.userId
            target_user = User.objects.get(userId=userId.userId)
            new_point_balance = int(target_user.pointBalance) - int(amount)
            if new_point_balance < 0:
                outcome_code = "0099"
                new_point_balance = target_user.pointBalance
            User.objects.filter(userId=userId.userId).update(pointBalance=str(new_point_balance))

        return HttpResponse(target_user)
    except Exception as e:
        print (e)
        return HttpResponse(e)