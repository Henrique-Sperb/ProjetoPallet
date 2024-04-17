from django import forms
from .models import Cargo, Company, Voucher


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = [
            'vehicle_plate',
            'pallets_quantity',
            'number_nf',
            'driver',
            'shipment_date',
            'unloading_date',
            'origin_company',
            'destination_company',
            'sale_or_disposal',
            'voucher',
        ]

    def clean_vehicle_plate(self):
        vehicle_plate = self.cleaned_data.get('vehicle_plate')
        # Adicione sua lógica de validação aqui. Por exemplo:
        if len(vehicle_plate) != 7:
            raise forms.ValidationError("A placa do veículo deve ter 7 caracteres.")
        return vehicle_plate


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = '__all__'
