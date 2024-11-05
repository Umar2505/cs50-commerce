from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=128)
    price = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    owner = User.username