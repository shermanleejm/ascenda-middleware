from rest_framework import serializers
from .models import *

"""
https://www.django-rest-framework.org/tutorial/1-serialization/
"""

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', "firstName", "lastName", "partnerCode", "pointBalance"]


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = "__all__"

class LoyaltyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyProgram
        # fields = ['bank_list', "loyaltyProgramId", "loyaltyProgramName", "loyaltyCurrencyName", "processingTime", "description", "enrollmentLink", "termsAndConditionsLink", "ratio"]
        fields = "__all__"

    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        # fields = ["referenceNumber", "membershipNumber", "partnerCode", "transactionDate", "transferAmount", "additionalInfo", "outcomeCode"]
        fields = "__all__"
    pass

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        # fields = ["userId", "loyaltyProgramId","membershipNumber"]
        fields = "__all__"
    pass
