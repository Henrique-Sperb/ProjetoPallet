from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Company
from django.shortcuts import get_object_or_404, redirect
from datetime import date


class CompanyListView(ListView):
    model = Company


class CompanyCreateView(CompanyListView):
    model = Company
    fields = [""]
