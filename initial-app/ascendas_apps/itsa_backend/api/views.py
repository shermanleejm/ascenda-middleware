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

import boto3
import tempfile
import shutil
import json
import random
import string
import requests
import csv

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.
"""
USER METHODS
"""
@csrf_exempt
def user_list(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)

"""
BANK METHODS
"""
@csrf_exempt
def bank_list(request):
    if request.method == "GET":
        banks = Bank.objects.all()
        serializer = BankSerializer(banks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BankSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def bank_detail(request, pk):
    try:
        bank = Bank.objects.get(pk=pk)
    except Bank.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BankSerializer(bank)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BankSerializer(bank, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        bank.delete()
        return HttpResponse(status=204)

"""
LOYALTY PROGRAM METHODS
"""
@csrf_exempt
def loyaltyprogram_list(request):
    if request.method == "GET":
        loyaltyprograms = LoyaltyProgram.objects.all()
        serializer = LoyaltyProgramSerializer(loyaltyprograms, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LoyaltyProgramSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def loyaltyprogram_detail(request, pk):
    try:
        loyaltyprogram = LoyaltyProgram.objects.get(pk=pk)
    except LoyaltyProgram.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LoyaltyProgramSerializer(loyaltyprogram)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LoyaltyProgramSerializer(loyaltyprogram, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        loyaltyprogram.delete()
        return HttpResponse(status=204)



"""
TRANSACTION METHODS
"""

@csrf_exempt
def transaction_list(request):
    if request.method == "GET":
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def transaction_detail(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(transaction, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        transaction.delete()
        return HttpResponse(status=204)

status_codes = {
    "0000" : "success",
    "0001" : "member not found",
    "0002" : "member name mismatch",
    "0003" : "member account closed",
    "0004" : "member account suspended",
    "0005" : "member ineligible for accrual",
    "0099" : "unable to process, please contact support for more information"
}
@csrf_exempt
def get_transaction_status(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        status = transaction.outcomeCode
        if status == None:
            resp = {"status" : "awaiting response from loyalty partner"}
            return JsonResponse(resp)
        resp = {"status" : status_codes[status]}
        return JsonResponse(resp)


@csrf_exempt
def get_transaction_by_user(request, userid):
    if request.method == 'GET':
        try:
            memberships = Membership.objects.filter(userId=userid)
            membership_id = [membership.membershipNumber for membership in memberships]
        except Membership.DoesNotExist:
            return HttpResponse(status=404)
        try:
            transactions = Transaction.objects.filter(membershipNumber__in = membership_id)
        except Transaction.DoesNotExist:
            return HttpResponse(status=404)
        
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def get_transaction_by_date(request, date):
    date = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
    try:
        transactions = Transaction.objects.filter(transactionDate=date)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)


"""
MEMBERSHIP METHODS
"""

@csrf_exempt
def membership_list(request):
    if request.method == "GET":
        memberships = Membership.objects.all()
        serializer = MembershipSerializer(memberships, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MembershipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



@csrf_exempt
def membership_detail(request, pk):
    try:
        membership = Membership.objects.get(pk=pk)
    except Membership.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MembershipSerializer(membership)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MembershipSerializer(membership, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        membership.delete()
        return HttpResponse(status=204)

@csrf_exempt
def get_membership_by_user_loyaltyprogram(request, userId, loyaltyId):
    try:
        membership = Membership.objects.get(userId = userId, loyaltyProgramId=loyaltyId)
    except Membership.DoesNotExist:
        return HttpResponse(status=404)

    serializer = MembershipSerializer(membership)
    return JsonResponse(serializer.data)
    