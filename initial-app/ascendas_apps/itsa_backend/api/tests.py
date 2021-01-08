from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
# Create your tests here.

class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('user-list')
        data = {
            "firstName" : "John",
            "lastName" : "Wick",
            "partnerCode" : "01377224",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().firstName, 'John')

class BankTests(APITestCase):
    def test_create_bank(self):
        """
        Ensure we can create a new bank object.
        """
        url = reverse('bank-list')
        data = {
            "name" : "123 bank",
            "partnerCode" : "123-bank-code",
            "loyaltyPrograms" : "loyalty"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bank.objects.count(), 1)
        self.assertEqual(Bank.objects.get().partnerCode, '123-bank-code')
    


class LoyaltyProgramTests(APITestCase):
    def test_create_loyaltyprogram(self):
        """
        Ensure we can create a new loyalty program object.
        And check that the corresponding bank objects are updated
        """
        url = reverse('loyaltyprogram-list')
        data = {
            "loyaltyProgramName" : "Loyalty 1",
            "loyaltyProgramId" : 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoyaltyProgram.objects.count(), 1)
        



    

# class TransactionTest(APITestCase):

#     def test_get_transaction_by_user(self):
#         bank = Bank.objects.create(name="test", partnerCode="123-bank-code")
#         user = User.objects.create(firstName="test", lastName="test", bankAccountId="123123", pointBalance="123123")
#         loyaltyprog = LoyaltyProgram.objects.create(bankCode=bank, loyaltyProgramName="test", loyaltyCurrencyName="test", description="sdfsd", enrollmentLink="sdfsdf", termsAndConditionLink="stet")

#         membership = Membership.objects.create(userId=user, loyaltyProgramId=loyaltyprog, membershipNumber="1")
#         transaction= Transaction.objects.create(referenceNumber="123", membershipNumber=membership, partnerCode=bank, transactionDate="20201212", transactionAmount="123", additionalInfo="123")

#         url = reverse('get-transaction-by-user')
#         response = self.client.get(url+"1")
#         self.assertEqual(r)
