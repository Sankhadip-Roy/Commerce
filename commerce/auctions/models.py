from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length=30)

    def __str__(self):
        return self.categoryName

class AuctionListing(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.URLField(max_length=200)

    isActive = models.BooleanField(default=True)

    Owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")

    date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Bids(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=True, null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f"{self.listing} | {self.bidder} | {self.amount}"


class Comments(models.Model):
    comment = models.CharField(max_length=300, blank=True, null=True)
    commentator = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey('AuctionListing', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"{self.product} | {self.commentator}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username} | {self.listing.name}"