from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "quantity", "created_at", "updated_at"]
    list_filter = ["location", "created_at", "updated_at"]
    search_fields = ["name", "description", "location__name"]
    readonly_fields = ["created_at", "updated_at"]
