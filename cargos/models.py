from django.db import models, transaction
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

    @transaction.atomic
    def save(self, *args, **kwargs):
        # O django gera uma Chave Primária "pk" para todos os objetos salvos no banco de dados.
        # Se o Cargo passado como parâmetro já tiver sido salvo no banco, terá essa coluna
        # permitindo o Django identificar se é um novo objeto ou está sendo atualizado.

        # is_new será True caso a coluna pk seja None, simbolizando um novo objeto.
        is_new = self.pk is None

        # Se is_new for True.
        if is_new:
            # Verifica se o carregamento é uma transferência, devolução ou um carregamento vindo
            # direto de um embarcador e atualiza o estoque e o saldo das empresas de origem e destino.
            if (
                self.is_transfer()
                or self.is_devolution()
                or self.is_shipper_branch_cargo()
            ):
                self.update_company_pallets(self.origin_company, self.pallets_quantity)
                self.update_company_pallets(
                    self.destination_company, -self.pallets_quantity
                )
            # Verifica se é um carregamento de longo curso.
            elif self.is_long_haul():
                # Se as opções vale pallet ou venda/descarte foram marcadas, não altera o estoque da filial responsável.
                if self.voucher or self.sale_or_disposal:
                    self.update_company_pallets(
                        self.origin_company, self.pallets_quantity
                    )
                    self.update_company_pallets(
                        self.responsible_branch, -self.pallets_quantity, False
                    )
                # Se não for gerado vale pallet, atualiza saldo e estoque.
                else:
                    self.update_company_pallets(
                        self.origin_company, self.pallets_quantity
                    )
                    self.update_company_pallets(
                        self.responsible_branch, -self.pallets_quantity
                    )
            # Simboliza que é uma entrega de uma filial para um cliente final.
            else:
                # Se foi gerado um vale ou houve venda/descarte dos pallets, diminuirá o estoque.
                if self.voucher or self.sale_or_disposal:
                    self.responsible_branch.pallets_storage -= self.pallets_quantity
                    self.responsible_branch.save()
                # Se não foi gerado um vale e não houve venda/descarte,
                # considera-se que os pallets retornaram para a filial, logo nenhum campo deve ser alterado.

            debt, created = Debt.objects.get_or_create(
                debtor=self.responsible_branch,
                creditor=self.associated_shipper,
                defaults={"amount": self.pallets_quantity},
            )

            # Se created for False, significa que a dívida já existia e atualiza a quantidade.
            debt.update_debt(self.pallets_quantity, is_devolution=self.is_devolution())

            # Se for uma transferência, atualiza a dívida da filial de origem
            if self.is_transfer():
                debt_sending_branch, created = Debt.objects.get_or_create(
                    debtor=self.origin_company,
                    creditor=self.associated_shipper,
                    defaults={"amount": 0},
                )
                debt_sending_branch.update_debt(self.pallets_quantity)

        # Se is_new for False.
        if not is_new:
            # Realiza uma busca no banco de dados e atribui a variável orig
            # o carregamento que tenha a mesma chave primária.
            orig = Cargo.objects.select_related(
                "origin_company", "destination_company"
            ).get(pk=self.pk)

            # Calcula a diferença entre a quantidade de pallets do objeto original e a do valor atual.
            # Se a quantidade original for maior que a atual, a diferença é negativa para representar uma redução.
            # Caso contrário, a diferença é positiva (em valor absoluto) para representar um aumento.
            if orig.pallets_quantity > self.pallets_quantity:
                pallets_difference = -(orig.pallets_quantity - self.pallets_quantity)
            else:
                pallets_difference = abs(orig.pallets_quantity - self.pallets_quantity)
            # Verifica através dos métodos se o carregamento é uma transferência, devolução ou um carregamento vindo
            # direto de um embarcador e atualiza o estoque e o saldo das empresas de origem e destino.
            if (
                self.is_transfer()
                or self.is_devolution()
                or self.is_shipper_branch_cargo()
            ):
                orig.update_company_pallets(self.origin_company, pallets_difference)
                orig.update_company_pallets(
                    self.destination_company, -pallets_difference
                )
            # Verifica se é um carregamento de longo curso.
            elif self.is_long_haul():
                # Se as opções vale pallet ou venda/descarte foram marcadas, não altera o estoque da filial responsável.
                if self.voucher:
                    orig.update_company_pallets(self.origin_company, pallets_difference)
                    orig.update_company_pallets(
                        self.responsible_branch, -pallets_difference, False
                    )
                # Se não for gerado vale pallet, atualiza saldo e estoque.
                else:
                    orig.update_company_pallets(self.origin_company, pallets_difference)
                    orig.update_company_pallets(
                        self.responsible_branch, -pallets_difference
                    )
            # Simboliza que é uma entrega de uma filial para um cliente final.
            else:
                # Se foi gerado um vale ou houve venda/descarte dos pallets, diminuirá o estoque.
                if self.voucher or self.sale_or_disposal:
                    self.responsible_branch.pallets_storage -= self.pallets_quantity
                    self.responsible_branch.save()
                # Se não foi gerado um vale e não houve venda/descarte,
                # considera-se que os pallets retornaram para a filial, logo nenhum campo deve ser alterado.

            # A função get_or_create busca no banco de dados um objeto com os parâmetros informados,
            # se o objeto não existir ele será criado com os valores informados e a variável created receberá True,
            # mas caso o objeto exista, seus valores serão atribuídos a variável debt, e created receberá False.
            debt, created = Debt.objects.get_or_create(
                debtor=self.responsible_branch,
                creditor=self.associated_shipper,
                defaults={"amount": self.pallets_quantity},
            )

            # Se created for False, significa que a dívida já existia e atualiza a quantidade.
            debt.update_debt(pallets_difference, is_devolution=self.is_devolution())

            # Se for uma transferência, atualiza a dívida da filial de origem
            if self.is_transfer():
                debt_sending_branch, created = Debt.objects.get_or_create(
                    debtor=self.origin_company,
                    creditor=self.associated_shipper,
                    defaults={"amount": 0},
                )
                debt_sending_branch.update_debt(pallets_difference)

        super().save(*args, **kwargs)

        # Se a opção voucher foi marcada, criará automaticamente um vale onde a empresa emissora é a empresa de destino
        # e a empresa recebedora é a filial responsável.
        if self.voucher:
            Voucher.objects.create(
                cargo=self,
                issuer=self.destination_company,
                recipient=self.responsible_branch,
                pallets=self.pallets_quantity,
                issue_date=self.unloading_date,
            )

    # Verifica se é um carregamento de longo curso e retorna True ou False.
    def is_long_haul(self):
        return (
            not self.origin_company.is_reiter_branch
            and not self.destination_company.is_reiter_branch
            and self.destination_company != self.associated_shipper
        )

    # Verifica se é uma devolução ao embarcador e retorna True ou False.
    def is_devolution(self):
        return (
            self.origin_company.is_reiter_branch
            and self.destination_company == self.associated_shipper
        )

    # Verifica se é uma transferência entre filiais e retorna True ou False.
    def is_transfer(self):
        return (
            self.origin_company.is_reiter_branch
            and self.destination_company.is_reiter_branch
        )

    # Verifica se é um carregamento vindo de um embarcador para uma filial e retorna True ou False.
    def is_shipper_branch_cargo(self):
        return (
            not self.origin_company.is_reiter_branch
            and self.destination_company.is_reiter_branch
        )

    # Método para atualizar o estoque e saldo da empresa passada como parâmetro. O atributo att_storage é True por
    # padrão, mas caso um vale seja gerado ou ocorra venda/descarte, deverá ser passado False na chamada do método.
    def update_company_pallets(self, company, pallets_difference, att_storage=True):
        if att_storage:
            company.pallets_storage -= pallets_difference
        company.pallets_balance += pallets_difference
        company.save()


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
    appointment_date = models.DateField(
        null=True, blank=True, verbose_name="DATA PREVISTA DE RECEBIMENTO"
    )
    receipt_date = models.DateField(
        null=True, blank=True, verbose_name="DATA DE RECEBIMENTO"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Chama o método save padrão

        # Verifica se o voucher foi recebido (se a data de recebimento está preenchida)
        if self.receipt_date:
            self.update_stock()

    def update_stock(voucher):
        if voucher.receipt_date:
            recipient = voucher.recipient
            recipient.pallets_storage += voucher.pallets
            recipient.save()


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
    amount = models.IntegerField(verbose_name="VALOR DA DÍVIDA")

    def update_debt(self, amount, is_devolution=False):
        # Atualiza a dívida com base na quantidade e no tipo de operação.
        if is_devolution:
            self.amount -= amount
        else:
            self.amount += amount
        self.save()
