from django.db import models


class Company(models.Model):
    name = models.CharField(
        blank=False, max_length=50, default="Empresa", verbose_name="NOME"
    )
    pallets_balance = models.IntegerField(
        default=0, verbose_name="SALDO DE PALLETS"
    )
    pallets_storage = models.IntegerField(
        default=0, verbose_name="ESTOQUE DE PALLETS"
    )

    def __str__(self):
        return self.name


class Driver(models.Model):
    driver_name = models.CharField(
        blank=False, null=False, max_length=50, verbose_name="NOME"
    )
    address = models.CharField(
        blank=False, null=False, max_length=100, default="Bairro, Cidade - UF", verbose_name="ENDEREÇO"
    )

    def __str__(self):
        return self.driver_name
