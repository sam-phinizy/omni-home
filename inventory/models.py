from django.db import models
from django.conf import settings


class Inventory(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(
        "locations.Location",
        on_delete=models.CASCADE,
        related_name="inventory_items"
    )
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_items'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_items'
    )

    class Meta:
        verbose_name_plural = "Inventory"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.quantity}) at {self.location}"
