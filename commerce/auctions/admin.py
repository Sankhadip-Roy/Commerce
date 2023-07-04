from django.contrib import admin

# Register your models here.
from .models import AuctionListing, Category

admin.site.register(AuctionListing)
admin.site.register(Category)