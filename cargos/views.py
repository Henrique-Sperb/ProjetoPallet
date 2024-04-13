from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cargo, Voucher


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


class VoucherListView(ListView):
    model = Voucher


class VoucherCreateView(CreateView):
    model = Voucher
    fields = [
        "issuer",
        "recipient",
        "pallets",
        "issue_date",
    ]
    success_url = reverse_lazy("voucher_list")


class VoucherUpdateView(UpdateView):
    model = Voucher
    fields = [
        "issuer",
        "recipient",
        "pallets",
        "issue_date",
    ]
    success_url = reverse_lazy("voucher_list")


class VoucherDeleteView(DeleteView):
    model = Voucher
    success_url = reverse_lazy("voucher_list")
