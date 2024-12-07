from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        if self.parent:
            return f"{self.name} (in {self.parent})"
        return self.name

    def get_full_path(self):
        """Returns the full path of nested locations (e.g., 'Basement > Rear > Box 1')"""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name
