from django.db import models

from catalog.models import Lure, Color


class CartItem(models.Model):
    product = models.ForeignKey(Lure, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.color}"

