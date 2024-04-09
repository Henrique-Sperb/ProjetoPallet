from django.contrib import admin
from django.urls import path
from cargos.views import cargos_list

urlpatterns = [path("admin/", admin.site.urls), path("", cargos_list)]
