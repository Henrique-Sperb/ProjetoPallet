from django.contrib import admin
from django.urls import path
from cargos.views import (
    CargoListView,
    CargoCreateView,
    CargoUpdateView,
    CargoDeleteView,
    VoucherListView,
    VoucherCreateView,
    VoucherUpdateView,
    VoucherDeleteView,
    CompanyDebtListView,
    ShipperDebtListView,
)

from companys.views import (
    CompanyListView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "company/<int:pk>/debts/", CompanyDebtListView.as_view(), name="company_debts"
    ),
    path("", CargoListView.as_view(), name="cargo_list"),
    path("novo_carregamento", CargoCreateView.as_view(), name="cargo_create"),
    path(
        "atualizar_carregamento/<int:pk>",
        CargoUpdateView.as_view(),
        name="cargo_update",
    ),
    path(
        "excluir_carregamento/<int:pk>", CargoDeleteView.as_view(), name="cargo_delete"
    ),
    path("lista_de_empresas", CompanyListView.as_view(), name="company_list"),
    path("nova_empresa", CompanyCreateView.as_view(), name="company_create"),
    path(
        "atualizar_empresa/<int:pk>",
        CompanyUpdateView.as_view(),
        name="company_update",
    ),
    path(
        "excluir_empresa/<int:pk>", CompanyDeleteView.as_view(), name="company_delete"
    ),
    path("lista_de_vales", VoucherListView.as_view(), name="voucher_list"),
    path("novo_vale", VoucherCreateView.as_view(), name="voucher_create"),
    path(
        "atualizar_vale/<int:pk>",
        VoucherUpdateView.as_view(),
        name="voucher_update",
    ),
    path(
        "excluir_vale/<int:pk>",
        VoucherDeleteView.as_view(),
        name="voucher_delete",
    ),
]
