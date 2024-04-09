from django.db import models


class Cargo(models.Model):
    shipment_date = models.DateField(blank=False, verbose_name="Data de Envio")
    unloading_date = models.DateField(null=True, verbose_name="Data de Recebimento", blank=True)
    pallets_quantity = models.IntegerField(blank=False, verbose_name="Quantidade de Pallets")
    origin_company = models.CharField(
        blank=False, max_length=50, verbose_name="Empresa de Origem"
    )
    destination_company = models.CharField(
        blank=False, max_length=50, verbose_name="Empresa de Destino"
    )
    number_nf = models.IntegerField(
        blank=False, verbose_name="Número da Nota Fiscal"
    )
    driver = models.CharField(
        blank=False, max_length=50, verbose_name="Nome do Motorista"
    )
    sale_or_disposal = models.BooleanField(
        default=False, verbose_name="Os pallets foram vendidos ou descartados?"
    )
