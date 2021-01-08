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
from django.db import connection

import random

def addFakeDataUtil():
    # fake user data
    # user_id, first_name, last_name
    temp_user = [
        (1, 'michael', 'jackson'),
        (2, 'freddie', 'mercury'),
        (3, 'beethoven', 'paul'),
    ]

    for i in range(len(temp_user)):
        new_user = User(
            firstName=temp_user[i][1],
            lastName=temp_user[i][2],
            partnerCode="dbs",
            pointBalance = 10000000000
        )
        new_user.save()

    LoyaltyProgram.objects.create(loyaltyProgramId="indopacific miles", loyaltyProgramName="indopacific miles")
    LoyaltyProgram.objects.create(loyaltyProgramId="quantum airlines qflyer", loyaltyProgramName="quantum airlines qflyer")
    LoyaltyProgram.objects.create(loyaltyProgramId="gojet points", loyaltyProgramName="gojet points")
    LoyaltyProgram.objects.create(loyaltyProgramId="eminent airways guest", loyaltyProgramName="eminent airways guest")
    

    new_bank = Bank(
        name="Digital Bank Singapore",
        partnerCode="dbs",
        loyaltyPrograms="indopacific miles",
    )
    new_bank.save()
    new_bank = Bank(
        name="Digital Bank Singapore",
        partnerCode="dbs",
        loyaltyPrograms="quantum airlines qflyer",
    )
    new_bank.save()
    new_bank = Bank(
        name="Digital Bank Singapore",
        partnerCode="dbs",
        loyaltyPrograms="gojet points",
    )
    new_bank.save()
    new_bank = Bank(
        name="Digital Bank Singapore",
        partnerCode="dbs",
        loyaltyPrograms="eminent airways guest",
    )
    new_bank.save()


    temp_data = [
        {
            'loyaltyProgramId': 'gojet points',
            'membershipNumber': '2153642985'
        },
        {
            'loyaltyProgramId': 'indopacific miles',
            'membershipNumber': '1567894821'
        },
        {
            'loyaltyProgramId': 'eminent airways guest',
            'membershipNumber': '100097739895'
        },
        {
            'loyaltyProgramId': 'quantum airlines qflyer',
            'membershipNumber': '8799420828'
        }
    ]

    for loyaltyProgramDetails in temp_data:
        t_user = User.objects.get(userId=1)

        new_membership = Membership(
            userId=t_user,
            loyaltyProgramId=loyaltyProgramDetails['loyaltyProgramId'],
            membershipNumber=loyaltyProgramDetails['membershipNumber']
        )
        new_membership.save()

def recreateDb():
    print("Wiping database")
    dbinfo = settings.DATABASES['default']
    print(dbinfo)

    # Postgres version
    #conn = db.connect(host=dbinfo['HOST'], user=dbinfo['USER'],
    #                 password=dbinfo['PASSWORD'], port=int(dbinfo['PORT'] or 5432))
    #conn.autocommit = True
    #cursor = conn.cursor()
    #cursor.execute("DROP DATABASE " + dbinfo['NAME'])
    #cursor.execute("CREATE DATABASE " + dbinfo['NAME'] + " WITH ENCODING 'UTF8'") # Default is UTF8, but can be changed so lets be sure.

    # Mysql version:
    print("Dropping and creating database " + dbinfo['NAME'])
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE " + dbinfo["NAME"] + "; CREATE DATABASE " + dbinfo["NAME"] + "; USE " + dbinfo["NAME"] + ";")
    print("Done")

@csrf_exempt
def addFakeData(request):
    try:
        if request.method == "GET":
            # fake user data
            # user_id, first_name, last_name
            addFakeDataUtil();
            print("added fake data")

    except Exception as e:
        print (e)

    return HttpResponse("success", 203)

# @csrf_exempt
# def resetDbAndAddFakeData(request):
#     try:
#         if request.method == "GET":
#             # fake user data
#             # user_id, first_name, last_name
#             recreateDb();
#             addFakeDataUtil();

#     except Exception as e:
#         print (e)

#     return HttpResponse("success", 203)

