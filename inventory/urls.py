from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('inventory/<int:item_number>/', views.InventoryDetailView.as_view(), name='detail'),
] 