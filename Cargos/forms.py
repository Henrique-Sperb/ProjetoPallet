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

        # Se a empresa de origem não é uma filial da Reiter, define o associated_shipper como a empresa de origem
        if origin_company and not origin_company.is_reiter_branch:
            cleaned_data["associated_shipper"] = origin_company

        # Se a empresa de destino é uma filial da Reiter, define o responsible_branch como a empresa de destino
        if destination_company and destination_company.is_reiter_branch:
            cleaned_data["responsible_branch"] = destination_company

        return cleaned_data


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = "__all__"
