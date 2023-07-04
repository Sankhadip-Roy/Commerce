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

    def __str__(self):
        return self.name


class Bids(models.Model):
    pass


class Comments(models.Model):
    comment = models.TextField(null=True)
