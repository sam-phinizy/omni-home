from django.contrib import admin
from .models import Inventory, InventoryType


@admin.register(InventoryType)
class InventoryTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "key", "created_at", "updated_at"]
    search_fields = ["name", "key"]
    prepopulated_fields = {"key": ("name",)}


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "quantity", "get_types", "created_by", "created_at", "updated_by", "updated_at"]
    list_filter = ["location", "types", "created_by", "updated_by", "created_at", "updated_at"]
    search_fields = ["name", "description", "location__name", "created_by__email", "updated_by__email"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]
    filter_horizontal = ['types']

    def get_types(self, obj):
        return ", ".join([t.name for t in obj.types.all()])
    get_types.short_description = "Types"

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
