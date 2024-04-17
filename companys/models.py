from django.db import models


class Company(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="NOME"
    )
    pallets_balance = models.IntegerField(verbose_name="SALDO DE PALLETS")
    pallets_storage = models.IntegerField(verbose_name="ESTOQUE DE PALLETS")

    def __str__(self):
        return self.name

    def get_issued_vouchers(self):
        return self.issued_vouchers.all()

    def get_received_vouchers(self):
        return self.received_vouchers.all()
