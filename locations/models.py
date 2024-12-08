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
        """Returns a list of strings representing the full path of nested locations."""
        path = []
        current_location = self
        while current_location:
            path.append(current_location.name)
            current_location = current_location.parent
        return path[::-1]  # Reverse the list to get the correct order
