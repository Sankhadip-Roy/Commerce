from django.contrib import admin

# Register your models here.
from .models import AuctionListing, Category, User

admin.site.register(AuctionListing)
admin.site.register(Category)
admin.site.register(User)