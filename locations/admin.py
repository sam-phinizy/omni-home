from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'floor')
    list_filter = ('floor',)
    search_fields = ('name',) 