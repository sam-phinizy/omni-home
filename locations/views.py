from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Location, InventoryItem


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'city', 'state', 'postal_code', 'country', 'notes']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'address',
            Row(
                Column('city', css_class='col-md-6'),
                Column('state', css_class='col-md-6'),
                css_class='row'
            ),
            Row(
                Column('postal_code', css_class='col-md-6'),
                Column('country', css_class='col-md-6'),
                css_class='row'
            ),
            'notes',
        )


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'locations/location_list.html'
    context_object_name = 'locations'
    ordering = ['name']


class LocationDetailView(LoginRequiredMixin, DetailView):
    model = Location
    template_name = 'locations/location_detail.html'


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'


class InventoryListView(ListView):
    model = InventoryItem
    template_name = 'locations/inventory_list.html'
    context_object_name = 'inventory_items' 