from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# models.py

from django.db import models
from django.contrib.auth.models import User


class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username} - {self.stock}"
