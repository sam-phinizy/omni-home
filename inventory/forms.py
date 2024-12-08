from django import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["name", "description", "quantity", "location", "types"]
        default_quantity = 1
