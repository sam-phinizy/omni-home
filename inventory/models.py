from django.db import models


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

    class Meta:
        verbose_name_plural = "Inventory"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.quantity}) at {self.location}"
