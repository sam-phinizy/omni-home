from django.urls import path
from . import views
from .views import InventoryListView

urlpatterns = [
    path('', views.LocationListView.as_view(), name='location_list'),
    path('<int:pk>/', views.LocationDetailView.as_view(), name='location_detail'),
    path('new/', views.LocationCreateView.as_view(), name='location_create'),
    path('<int:pk>/edit/', views.LocationUpdateView.as_view(), name='location_edit'),
    path('inventory/', InventoryListView.as_view(), name='inventory_list'),
] 