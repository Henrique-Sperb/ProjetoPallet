from django.db import models


class Company(models.Model):
    cnpj = models.IntegerField()
    address = models.CharField(max_length=100)
    pallet_balance = models.IntegerField()


class ReiterBranch(Company):
    pallet_storage = models.IntegerField()


class ShipperBranch(Company):
    pass


class FinalCustomerBranch(Company):
    pass
