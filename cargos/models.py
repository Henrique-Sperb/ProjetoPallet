from django.db import models
from companys.models import Company, Driver


class Cargo(models.Model):
    vehicle_plate = models.CharField(
        null=False,
        blank=False,
        default="AAA1A11",
        max_length=7,
        verbose_name="PLACA DO VEICULO",
    )
    pallets_quantity = models.IntegerField(
        blank=False, verbose_name="QUANTIDADE DE PALLETS"
    )
    number_nf = models.IntegerField(
        blank=True, null=True, verbose_name="Nº DA NOTA FISCAL"
    )
    driver = models.ForeignKey(
        Driver,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="NOME DO MOTORISTA",
    )
    shipment_date = models.DateField(blank=False, verbose_name="DATA DE ENVIO")
    unloading_date = models.DateField(
        null=True, verbose_name="DATA DE RECEBIMENTO", blank=True
    )
    origin_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="origin_cargos",
        verbose_name="EMPRESA DE ORIGEM",
    )
    destination_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="destination_cargos",
        verbose_name="EMPRESA DE DESTINO",
    )
    sale_or_disposal = models.BooleanField(
        default=False, verbose_name="OS PALLETS FORAM VENDIDOS OU DESCARTADOS?"
    )
    voucher = models.BooleanField(
        default=False, verbose_name="O CLIENTE FINAL GEROU VALE PALLET?"
    )
