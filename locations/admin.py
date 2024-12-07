from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'get_full_path', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name', 'description', 'parent__name']
    readonly_fields = ['created_at', 'updated_at'] 