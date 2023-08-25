from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='colors/')

    def __str__(self):
        return self.name


class Lure(models.Model):
    name = models.CharField(max_length=100)
    colors = models.ManyToManyField(Color)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
