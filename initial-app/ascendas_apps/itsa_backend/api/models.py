from django.db import models
# Create your models here.

"""
all models so far are set up with default values, ie maxlength 50, can just change if required
TODO : get_absolute_url, verbose names
"""
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    partnerCode = models.CharField(max_length=50)
    pointBalance = models.CharField(max_length=50, default=10000)

    def __str__(self):
        return "User: {} {}".format(self.firstName, self.lastName)
    
class Bank(models.Model):
    name = models.CharField(max_length=50)
    partnerCode = models.CharField(primary_key=True,max_length=50)
    # loyaltyPrograms = models.ManyToManyField("LoyaltyProgram", related_name="bank_list", blank=True)
    loyaltyPrograms = models.CharField(max_length=50)

    def __str__(self):
        return "Bank: " + self.name

class LoyaltyProgram(models.Model):
    loyaltyProgramId = models.CharField(primary_key=True, max_length=100)
    loyaltyProgramName = models.CharField(max_length=50)
    loyaltyCurrencyName = models.CharField(max_length=50, default="SGD")
    processingTime = models.CharField(max_length=50, default="1 day") # not sure what this means, change field to datetime if needed
    description = models.CharField(max_length=50, default="description")
    enrollmentLink = models.CharField(max_length=50, default="test.com")
    termsAndConditionsLink = models.CharField(max_length=50, default="test.com")
    ratio = models.IntegerField(help_text="Ratio of bank points to loyalty program points", default=10)

    def __str__(self):
        return self.loyaltyProgramName
    

class Membership(models.Model):
    userId = models.ForeignKey(User, verbose_name="User ID", on_delete=models.CASCADE)
    # loyaltyProgramId = models.ForeignKey(LoyaltyProgram, verbose_name="Loyalty ID", on_delete=models.CASCADE)
    loyaltyProgramId = models.CharField(max_length=50)
    membershipNumber = models.CharField(max_length=50)
    loyaltyMembershipRef = models.AutoField(primary_key=True)

    def __str__(self):
        return "{} LoyaltyProgramID: {}".format(self.userId, self.loyaltyProgramId)

"""
Didnt include userid, loyaltyprogramid because can get from membership entity
can include if needed i think 
"""

class Transaction(models.Model):

    # referenceNumber = models.AutoField(primary_key=True) # change to AutoField
    # membershipNumber = models.ForeignKey(Membership, on_delete=models.CASCADE)
    # partnerCode = models.ForeignKey(Bank, on_delete=models.CASCADE)
    # # transactionDate = models.DateField(auto_now_add=True)
    # transactionDate = models.CharField(max_length=50)
    # transferAmount = models.CharField(max_length=50)
    # additionalInfo = models.CharField(max_length=50, blank=True)
    # outcomeCode = models.CharField(max_length=50, blank=True, null=True) # can change to enum next 
    # loyaltyProgramId = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, verbose_name="Loyalty ID")

    transactionId = models.AutoField(primary_key=True)
    referenceNumber = models.CharField(max_length=50) # change to AutoField
    membershipNumber = models.CharField(max_length=50)
    partnerCode = models.CharField(max_length=50)
    transactionDate = models.CharField(max_length=50)
    transferAmount = models.CharField(max_length=50)
    additionalInfo = models.CharField(max_length=50, blank=True)
    outcomeCode = models.CharField(max_length=50, blank=True, null=True) # can change to enum next 
    loyaltyProgramId = models.CharField(max_length=50)
    
    def __str__(self):
        return "Transaction {}".format(self.referenceNumber)

    

    


    


