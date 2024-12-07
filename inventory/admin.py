from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "quantity", "created_by", "created_at", "updated_by", "updated_at"]
    list_filter = ["location", "created_by", "updated_by", "created_at", "updated_at"]
    search_fields = ["name", "description", "location__name", "created_by__email", "updated_by__email"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
