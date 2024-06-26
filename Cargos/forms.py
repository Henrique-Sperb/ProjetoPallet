from django import forms
from .models import Cargo, Company, Voucher


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = [
            "vehicle_plate",
            "pallets_quantity",
            "number_nf",
            "driver",
            "shipment_date",
            "unloading_date",
            "origin_company",
            "destination_company",
            "sale_or_disposal",
            "voucher",
            "responsible_branch",
            "associated_shipper",
        ]

    def clean(self):
        cleaned_data = super().clean()
        origin_company = cleaned_data.get("origin_company")
        destination_company = cleaned_data.get("destination_company")

        # Se a empresa de origem não é uma filial da Reiter, define o associated_shipper como a empresa de origem.
        if not origin_company.is_reiter_branch:
            cleaned_data["associated_shipper"] = origin_company

        # Se a empresa de destino é uma filial da Reiter, define o responsible_branch como a empresa de destino.
        if destination_company.is_reiter_branch:
            cleaned_data["responsible_branch"] = destination_company

        # Se a empresa de origem é uma filial da Reiter e a empresa de destino não, define o responsible_branch como a
        # empresa de destino.
        if origin_company.is_reiter_branch and not destination_company.is_reiter_branch:
            cleaned_data["responsible_branch"] = origin_company

        # Se for uma transferência, devolução ou um carregamento vindo de um embarcador para uma filial, define os
        # campos voucher e sale_or_disposal como False, independente do que foi marcado no formulário.
        if self.is_transfer() or self.is_devolution() or self.is_shipper_branch_cargo():
            cleaned_data["voucher"] = False
            cleaned_data["sale_or_disposal"] = False

        return cleaned_data

    def is_devolution(self):
        origin_company = self.cleaned_data.get("origin_company")
        destination_company = self.cleaned_data.get("destination_company")
        associated_shipper = self.cleaned_data.get("associated_shipper")
        return (
            origin_company.is_reiter_branch
            and destination_company == associated_shipper
        )

    def is_transfer(self):
        origin_company = self.cleaned_data.get("origin_company")
        destination_company = self.cleaned_data.get("destination_company")
        return origin_company.is_reiter_branch and destination_company.is_reiter_branch

    def is_shipper_branch_cargo(self):
        origin_company = self.cleaned_data.get("origin_company")
        destination_company = self.cleaned_data.get("destination_company")
        return (
            not origin_company.is_reiter_branch and destination_company.is_reiter_branch
        )


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = "__all__"
