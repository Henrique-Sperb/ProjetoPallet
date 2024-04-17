from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cargo, Voucher
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
