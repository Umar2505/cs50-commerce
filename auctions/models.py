from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=128)
    price = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", blank=True)

class Bids(models.Model):
    price = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ManyToManyField(Listing, related_name="bids")