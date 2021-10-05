from django.db import models
from datetime import date
from django.utils import timezone
# Create your models here.
class InputData(models.Model):
    """docstring for InputData."""
    authKeys = models.CharField(unique=True,max_length=10)
    inputs = models.CharField(max_length=10000)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.authKeys
