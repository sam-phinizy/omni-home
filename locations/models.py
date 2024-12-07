from django.db import models


class Floor(models.IntegerChoices):
    BASEMENT = -1, "Basement"
    FIRST = 1, "First Floor"
    SECOND = 2, "Second Floor"
    THIRD = 3, "Third Floor"
    ATTIC = 4, "Attic"


class Location(models.Model):
    name = models.CharField(max_length=100)
    floor = models.IntegerField(choices=Floor.choices)

    def __str__(self):
        return f"{self.name} ({self.get_floor_display()})"

    class Meta:
        ordering = ["floor", "name"]
