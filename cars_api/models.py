from django.db import models


# Create your models here.
class Car(models.Model):
    model = models.CharField(max_length=90)
    price = models.CharField(max_length=90)
    year = models.CharField(max_length=90)
    mileage = models.CharField(max_length=90)

    def __str__(self):
        return self.model
