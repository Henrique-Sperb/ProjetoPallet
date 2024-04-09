from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Cargo
from django.shortcuts import get_object_or_404, redirect
from datetime import date


class CargoListView(ListView):
    model = Cargo


class CargoCreateView(CreateView):
    model = Cargo
    fields = [
        "sale_or_disposal",
        "pallets_quantity",
        "shipment_date",
        "unloading_date",
        "origin_company",
        "destination_company",
        "number_nf",
        "driver",
    ]
    success_url = reverse_lazy("cargo_list")


class CargoUpdateView(UpdateView):
    model = Cargo
    fields = [
        "sale_or_disposal",
        "pallets_quantity",
        "shipment_date",
        "unloading_date",
        "origin_company",
        "destination_company",
        "number_nf",
        "driver",
    ]
    success_url = reverse_lazy("cargo_list")


class CargoDeleteView(DeleteView):
    model = Cargo
    success_url = reverse_lazy("cargo_list")


class CargoConfirmView(View):
    def get(self, request, pk):
        cargo = get_object_or_404(Cargo, pk=pk)
        cargo.unloading_date = date.today()
        cargo.save()
        return redirect("cargo_list")
