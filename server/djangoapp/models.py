from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    COUPE = "Coupe"
    HATCHBACK = "Hatchback"
    TYPE_CHOICES = [(v, v) for v in [SEDAN, SUV, WAGON, COUPE, HATCHBACK]]
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SEDAN)
    year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2026)])

    class Meta:
        unique_together = ("make", "name", "year")

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.year})"
