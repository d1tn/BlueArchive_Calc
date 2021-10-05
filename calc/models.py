from django.db import models
from datetime import date
from django.utils import timezone
# Create your models here.
class InputData(object):
    """docstring for InputData."""
    authKeys = models.CharField(max_length=10)
    inputs = models.CharField(max_length=10000)
    date = models.DateTimeField(default=timezone.now)

    def __init__(self, arg):
        super(InputData, self).__init__()
        self.arg = arg
