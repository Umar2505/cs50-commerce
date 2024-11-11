from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=128)
    price = models.FloatField()
    img = models.CharField(blank=True, default="https://www.contentviewspro.com/wp-content/uploads/2017/07/default_image.png", max_length = 9999)
    date = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", blank=True)
    watchlist = models.ManyToManyField(User, related_name="watchlist", blank=True)
    category = models.CharField(blank=True, default="No Category Listed", max_length=128)
    inactive = models.BooleanField(blank=True, default=False)


class Bids(models.Model):
    price = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="bids")

class Comments(models.Model):
    text = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now=True)