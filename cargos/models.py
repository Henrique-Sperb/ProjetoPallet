from django.db import models


class Cargo(models.Model):
    shipment_date = models.DateField(blank=False)
    unloading_date = models.DateField(blank=True)
    pallets_quantity = models.IntegerField(blank=False)
    origin_company = models.CharField(blank=False, max_length=50)
    destination_company = models.CharField(blank=False, max_length=50)
    number_nf = models.CharField(blank=False, max_length=50)
    driver = models.CharField(blank=False, max_length=50)
    sale_or_disposal = models.BooleanField(blank=True)
