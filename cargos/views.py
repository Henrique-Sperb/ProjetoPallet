from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from companys.models import Company
from .models import Cargo, Voucher, Debt
from .forms import CargoForm, VoucherForm


class CargoListView(ListView):
    model = Cargo


class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargos/cargo_form.html'
    success_url = reverse_lazy("cargo_list")


class CargoUpdateView(UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargos/cargo_form.html'
    success_url = reverse_lazy("cargo_list")


class CargoDeleteView(DeleteView):
    model = Cargo
    success_url = reverse_lazy("cargo_list")


class VoucherListView(ListView):
    model = Voucher


class VoucherCreateView(CreateView):
    model = Voucher
    form_class = VoucherForm
    template_name = 'cargos/voucher_form.html'
    success_url = reverse_lazy("voucher_list")


class VoucherUpdateView(UpdateView):
    model = Voucher
    form_class = VoucherForm
    template_name = 'cargos/voucher_form.html'
    success_url = reverse_lazy("voucher_list")


class VoucherDeleteView(DeleteView):
    model = Voucher
    success_url = reverse_lazy("voucher_list")


class CompanyDebtListView(ListView):
    model = Debt
    template_name = 'debt_list.html'

    def get_queryset(self):
        company = get_object_or_404(Company, pk=self.kwargs.get('pk'))
        return company.get_debts()
