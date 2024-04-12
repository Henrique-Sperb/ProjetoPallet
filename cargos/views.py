from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cargo


class CargoListView(ListView):
    model = Cargo


class CargoCreateView(CreateView):
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
    ]
    success_url = reverse_lazy("cargo_list")


class CargoUpdateView(UpdateView):
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
    ]
    success_url = reverse_lazy("cargo_list")


class CargoDeleteView(DeleteView):
    model = Cargo
    success_url = reverse_lazy("cargo_list")
