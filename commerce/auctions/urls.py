from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:item_id>", views.item_details, name='item_details'),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_name>", views.products_by_category, name='products_by_category'),
    path("createListing", views.createListing, name="createListing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("updatewatchlist/<int:item_id>", views.update_watchlist, name="updatewatchlist")
]
