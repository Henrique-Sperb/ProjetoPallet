from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=30, verbose_name="NOME")
    pallets_balance = models.IntegerField(default=0, verbose_name="SALDO DE PALLETS")
    pallets_storage = models.IntegerField(default=0, verbose_name="ESTOQUE DE PALLETS")
    is_reiter_branch = models.BooleanField(verbose_name="É FILIAL DA REITER?")

    def __str__(self):
        return self.name

    def get_issued_vouchers(self):
        return self.issued_vouchers.all()

    def get_received_vouchers(self):
        return self.received_vouchers.all()

    def get_debts(self):
        return self.debts_owed.all()
