from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Location


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'locations/location_list.html'
    context_object_name = 'locations'

    def get_queryset(self):
        # Only show top-level locations (those without parents) by default
        return Location.objects.filter(parent=None).order_by('name')


class LocationDetailView(LoginRequiredMixin, DetailView):
    model = Location
    template_name = 'locations/location_detail.html'


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    template_name = 'locations/location_form.html'
    fields = ['name', 'parent', 'description']
    success_url = reverse_lazy('locations:list')


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    template_name = 'locations/location_form.html'
    fields = ['name', 'parent', 'description']
    success_url = reverse_lazy('locations:list')
