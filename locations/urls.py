from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('', views.LocationListView.as_view(), name='list'),
    path('<int:pk>/', views.LocationDetailView.as_view(), name='detail'),
    path('create/', views.LocationCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.LocationUpdateView.as_view(), name='edit'),
] 