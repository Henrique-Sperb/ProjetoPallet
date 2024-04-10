from django.contrib import admin
from django.urls import path
from cargos.views import (
    CargoListView,
    CargoCreateView,
    CargoUpdateView,
    CargoDeleteView,
    CargoConfirmView,
)

from companys.views import (CompanyListView, CompanyCreateView,
#    CompanyUpdateView,
#    CompanyDeleteView,
#    CompanyConfirmView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("lista_de_carregamentos", CargoListView.as_view(), name="cargo_list"),
    path("novo_carregamento", CargoCreateView.as_view(), name="cargo_create"),
    path("atualizar_carregamento/<int:pk>", CargoUpdateView.as_view(), name="cargo_update"),
    path("excluir_carregamento/<int:pk>", CargoDeleteView.as_view(), name="cargo_delete"),
    path("confirmar_exclusao/<int:pk>", CargoConfirmView.as_view(), name="cargo_confirm"),
    path("lista_de_empresas", CompanyListView.as_view(), name="companys_list"),
    path("novo_carregamento", CompanyCreateView.as_view(), name="cargo_create"),
    #path("atualizar_cadastro_empresa/<int:pk>", CompanyUpdateView.as_view(), name="company_update"),
    #path("excluir_empresa/<int:pk>", CompanyDeleteView.as_view(), name="company_delete"),
    #path("confirmar_exclusao/<int:pk>", CompanyConfirmView.as_view(), name="company_confirm"),
]
