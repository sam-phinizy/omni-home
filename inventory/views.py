from django.shortcuts import render
from django.views.generic import DetailView
from .models import Inventory

class InventoryDetailView(DetailView):
    model = Inventory
    template_name = 'inventory/inventory_detail.html'
    context_object_name = 'item'
    pk_url_kwarg = 'item_number'
