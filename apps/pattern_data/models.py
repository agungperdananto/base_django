from django.db import models

from utils.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    values = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)
