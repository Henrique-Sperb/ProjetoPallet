from django.contrib import admin
from django.urls import path
from cargos.views import (
    CargoListView,
    CargoCreateView,
    CargoUpdateView,
    CargoDeleteView,
)

from companys.views import (
    CompanyListView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView,
    DriverListView,
    DriverCreateView,
    DriverUpdateView,
    DriverDeleteView,
)

urlpatterns = [
    path(
        "admin/", admin.site.urls
    ),
    path(
        "lista_de_carregamentos", CargoListView.as_view(), name="cargo_list"
    ),
    path(
        "novo_carregamento", CargoCreateView.as_view(), name="cargo_create"
    ),
    path(
        "atualizar_carregamento/<int:pk>", CargoUpdateView.as_view(), name="cargo_update",
    ),
    path(
        "excluir_carregamento/<int:pk>", CargoDeleteView.as_view(), name="cargo_delete"
    ),
    path(
        "lista_de_empresas", CompanyListView.as_view(), name="company_list"
    ),
    path(
        "nova_empresa", CompanyCreateView.as_view(), name="company_create"
    ),
    path(
        "atualizar_cadastro_empresa/<int:pk>", CompanyUpdateView.as_view(), name="company_update",
    ),
    path(
        "excluir_empresa/<int:pk>", CompanyDeleteView.as_view(), name="company_delete"
    ),
    path(
        "lista_de_motoristas", DriverListView.as_view(), name="driver_list"
    ),
    path(
        "novo_motorista", DriverCreateView.as_view(), name="driver_create"
    ),
    path(
        "atualizar_cadastro_motorista/<int:pk>", DriverUpdateView.as_view(), name="driver_update",
    ),
    path(
        "excluir_motorista/<int:pk>", DriverDeleteView.as_view(), name="driver_delete"
    ),
]
