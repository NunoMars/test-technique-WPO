# operations/models.py

from django.db import models


class Operation(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField()
    restrictions = models.JSONField()
