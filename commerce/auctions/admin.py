from django.contrib import admin

# Register your models here.
from .models import AuctionListing, Category, User, Comments, Bids, Watchlist

admin.site.register(AuctionListing)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(Watchlist)