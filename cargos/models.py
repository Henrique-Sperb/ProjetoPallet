from django.db import models, transaction
from django.db.models import F
from companys.models import Company


class Cargo(models.Model):
    vehicle_plate = models.CharField(
        max_length=7,
        verbose_name="PLACA DO VEICULO",
    )
    pallets_quantity = models.IntegerField(verbose_name="QUANTIDADE DE PALLETS")
    number_nf = models.IntegerField(
        blank=True, null=True, verbose_name="Nº DA NOTA FISCAL"
    )
    driver = models.CharField(
        max_length=20,
        verbose_name="NOME DO MOTORISTA",
    )
    shipment_date = models.DateField(blank=False, verbose_name="DATA DE ENVIO")
    unloading_date = models.DateField(
        null=True, blank=True, verbose_name="DATA DE RECEBIMENTO"
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
        verbose_name="OS PALLETS FORAM VENDIDOS OU DESCARTADOS?"
    )
    voucher = models.BooleanField(verbose_name="O CLIENTE FINAL GEROU VALE PALLET?")
    responsible_branch = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="responsible_branch",
        verbose_name="FILIAL RESPONSÁVEL",
    )
    associated_shipper = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="associated_shipper",
        verbose_name="EMBARCADOR ASSOCIADO",
    )

    def update_company_pallets(self, company, pallets_quantity):
        company.pallets_storage = F("pallets_storage") + pallets_quantity
        company.pallets_balance = F("pallets_balance") - pallets_quantity

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not is_new:
            orig = Cargo.objects.select_related(
                "origin_company", "destination_company"
            ).get(pk=self.pk)
            self.update_company_pallets(orig.origin_company, orig.pallets_quantity)
            self.update_company_pallets(
                orig.destination_company, -orig.pallets_quantity
            )
            orig.origin_company.save()
            orig.destination_company.save()

        super().save(*args, **kwargs)

        self.update_company_pallets(self.origin_company, -self.pallets_quantity)
        self.update_company_pallets(self.destination_company, self.pallets_quantity)
        self.origin_company.save()
        self.destination_company.save()

        debt, created = Debt.objects.get_or_create(
            debtor=self.destination_company,
            creditor=self.associated_shipper,
            defaults={"amount": self.pallets_quantity},
        )

        if not created:
            # se a dívida já existir, atualiza a quantidade
            debt.amount += self.pallets_quantity
            debt.save()

        if (
            self.origin_company.is_reiter_branch
            and self.destination_company.is_reiter_branch
        ):
            # atualiza a dívida da filial que está enviando os pallets
            debt_sending_branch, created = Debt.objects.get_or_create(
                debtor=self.origin_company,
                creditor=self.associated_shipper,
                defaults={
                    "amount": 0
                },  # a quantidade padrão é 0 porque estamos reduzindo a dívida
            )

            # reduz a quantidade de dívida conforme a quantidade enviada
            debt_sending_branch.amount -= self.pallets_quantity
            debt_sending_branch.save()

        if is_new and self.voucher:
            Voucher.objects.create(
                cargo=self,
                issuer=self.origin_company,
                recipient=self.responsible_branch,
                pallets=self.pallets_quantity,
                issue_date=self.unloading_date,
            )


class Voucher(models.Model):
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.CASCADE,
        related_name="vouchers",
        verbose_name="CARREGAMENTO",
    )
    issuer = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="issued_vouchers",
        verbose_name="EMISSORA DO VALE",
    )
    recipient = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="received_vouchers",
        verbose_name="RECEBEDORA DO VALE",
    )
    pallets = models.IntegerField(null=False, blank=False, verbose_name="QUANTIDADE")
    issue_date = models.DateField(verbose_name="DATA DE EMISSÃO")
    receipt_date = models.DateField(
        null=True, blank=True, verbose_name="DATA DE RECEBIMENTO"
    )


class Debt(models.Model):
    debtor = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="debts_owed",
        verbose_name="EMPRESA DEVEDORA",
    )
    creditor = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="debts_due",
        verbose_name="EMPRESA CREDORA",
    )
    amount = models.IntegerField(verbose_name="QUANTIDADE DE DÍVIDA")
