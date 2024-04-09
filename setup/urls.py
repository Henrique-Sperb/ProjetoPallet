from django.contrib import admin
from django.urls import path
from cargos.views import (
    CargoListView,
    CargoCreateView,
    CargoUpdateView,
    CargoDeleteView,
    CargoConfirmView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("list", CargoListView.as_view(), name="cargo_list"),
    path("create", CargoCreateView.as_view(), name="cargo_create"),
    path("update/<int:pk>", CargoUpdateView.as_view(), name="cargo_update"),
    path("delete/<int:pk>", CargoDeleteView.as_view(), name="cargo_delete"),
    path("confirm/<int:pk>", CargoConfirmView.as_view(), name="cargo_confirm"),
]
