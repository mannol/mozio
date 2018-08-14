import re
import uuid

from django.core.exceptions import ValidationError
from django.contrib.gis.db import models

from mozio.apps.providers.models import Provider

class Area(models.Model):
    Provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    Name = models.CharField(max_length=2048)
    Price = models.FloatField()
    Polygon = models.PolygonField(db_index = True)

    def __str__(self):
        return '{} {}'.format(self.Name, self.Price)

    def to_dict(self):
        return {
            'name': self.Name,
            'price': self.Price,
            'provider': self.Provider.Name
        }

