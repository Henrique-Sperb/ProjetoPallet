from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.db.models import Sum
from companys.models import Company
from .models import Cargo, Voucher, Debt
from .forms import CargoForm, VoucherForm


class BaseCargoView:
    model = Cargo
    form_class = CargoForm
    template_name = "cargos/cargo_form.html"
    success_url = reverse_lazy("cargo_list")


class CargoListView(ListView):
    model = Cargo


class CargoCreateView(BaseCargoView, CreateView):
    pass


class CargoUpdateView(BaseCargoView, UpdateView):
    pass


class CargoDeleteView(DeleteView):
    model = Cargo
    success_url = reverse_lazy("cargo_list")


class BaseVoucherView:
    model = Voucher
    form_class = VoucherForm
    template_name = "cargos/voucher_form.html"
    success_url = reverse_lazy("voucher_list")


class VoucherListView(ListView):
    model = Voucher


class VoucherCreateView(BaseVoucherView, CreateView):
    pass


class VoucherUpdateView(BaseVoucherView, UpdateView):
    pass


class VoucherDeleteView(DeleteView):
    model = Voucher
    success_url = reverse_lazy("voucher_list")


class CompanyDebtListView(ListView):
    model = Debt
    template_name = "debt_list.html"

    def get_queryset(self):
        company = get_object_or_404(Company, pk=self.kwargs.get("pk"))
        if company.is_reiter_branch:
            return company.debts_owed.annotate(total_debt=Sum("amount")).order_by("-total_debt")
        else:
            return company.debts_due.annotate(total_debt=Sum("amount")).order_by("-total_debt")

    def get_context_data(self, **kwargs):
        if not hasattr(self, 'company'):
            self.company = get_object_or_404(Company, pk=self.kwargs.get("pk"))
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        return context


class ShipperDebtListView(ListView):
    model = Debt
    template_name = "home.html"

    def creditors(request):
        creditors = Company.objects.annotate(total_debt=Sum('debts__amount'))
        return render(request, 'home.html', {'creditors': creditors})
