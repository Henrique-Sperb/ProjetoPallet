from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Company, Driver


class CompanyListView(ListView):
    model = Company


class CompanyCreateView(CreateView):
    model = Company
    fields = [
        "name",
        "pallets_balance",
        "pallets_storage",
    ]
    success_url = reverse_lazy("company_list")


class CompanyUpdateView(UpdateView):
    model = Company
    fields = [
        "name",
        "pallets_balance",
        "pallets_storage",
    ]
    success_url = reverse_lazy("company_list")


class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy("company_list")


class DriverListView(ListView):
    model = Driver


class DriverCreateView(CreateView):
    model = Driver
    fields = [
        "driver_name",
        "address",
    ]
    success_url = reverse_lazy("driver_list")


class DriverUpdateView(UpdateView):
    model = Driver
    fields = ["driver_name", "address"]
    success_url = reverse_lazy("driver_list")


class DriverDeleteView(DeleteView):
    model = Driver
    success_url = reverse_lazy("driver_list")
