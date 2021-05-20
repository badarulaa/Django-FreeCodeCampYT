from typing import List
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sale
# Create your views here.

def home_view(request):
    hello = 'hello world from the view'
    return render(request, 'sales/home.html', {'hello':hello})

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/detail.html'