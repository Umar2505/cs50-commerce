from django.contrib import admin
from .models import User, Listing, Bids

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bids)