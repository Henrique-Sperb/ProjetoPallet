from django.shortcuts import render
from .models import Cargo


def cargos_list(request):
    cargos = Cargo.objects.all()
    return render(request, "Cargos/cargos_list.html", {"Cargos": cargos})
