from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, AuctionListing, Category, Comments, Bids, Watchlist
from .forms import CommentForm, BidForm


def index(request):
    context = {'items':AuctionListing.objects.all()}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def createListing(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        image = request.POST['image']
        category_id=request.POST['category']
        category = Category.objects.get(pk=category_id)
        product = AuctionListing(name=name, price=price, description=description, image=image, category=category)
        product.save()

        return redirect('index')
    else:
        categories = Category.objects.all()
        return render(request, "auctions/createListing.html", {'categories': categories})


def categories(request):
    context = {'categories':Category.objects.all()}
    return render(request, "auctions/categories.html",context)

def products_by_category(request, category_name):
    category = get_object_or_404(Category, categoryName=category_name)
    items=AuctionListing.objects.filter(category=category)
    context = {
        'category': category,
        'items': items
    }
    return render(request, 'auctions/products_by_category.html', context)

def item_details(request, item_id):
    item = AuctionListing.objects.get(id = item_id)

    #for bid
    bids = Bids.objects.filter(listing=item).order_by('-amount')
    highest_bid = item.highest_bid
    highest_bidder = item.highest_bidder
    error_msg=""
    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid_amount = bid_form.cleaned_data['amount']
            
            if (highest_bid is None or bid_amount > highest_bid) and bid_amount >= item.price:
                # Update the highest bid and bidder
                item.highest_bid = bid_amount
                item.highest_bidder = request.user
                item.save()

                # Create a new bid
                bid = Bids(listing=item, bidder=request.user, amount=bid_amount)
                bid.save()

                # Refresh the page to show the updated bid information
                return HttpResponseRedirect(request.path_info)
            else:
                if bid_amount < item.price:
                    error_msg="Please bid as minimum as the opening price"
                elif bid_amount < highest_bid:
                    error_msg="Please bid more than the last highest bidder"

    else:
        bid_form = BidForm()
        

    if request.method == "POST":
            comment = CommentForm(request.POST)
            if comment.is_valid():
                save_comment(request, comment.cleaned_data['comment'], item)

    your_comment = CommentForm()
    all_comments = Comments.objects.filter(product = item)
    context = {
        'item': item,
        'your_comment' : your_comment,
        'all_comments':all_comments,
        'bids': bids,
        'highest_bid': highest_bid,
        'highest_bidder': highest_bidder,
        'bid_form': bid_form,
        'bid_count':bids.count(),
        'error_msg': error_msg,
        'username': User.username
    }
    return render(request, 'auctions/item_details.html', context)

@login_required
def save_comment(request, content, product):
    commentator = User.objects.get(username = request.user.username)
    comment = Comments(comment=content, commentator=commentator, product=product)
    comment.save()

@login_required
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {"watchlist_items": watchlist_items})


@login_required
def add_to_watchlist(request, item_id):
    listing = get_object_or_404(AuctionListing, pk=item_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user, listing=listing)
    if created:
        messages.info(request, 'Added to watchlist.')
        # message = "Added to watchlist."
    else:
        messages.info(request, 'Already in watchlist.')
        # message = "Already in watchlist."
    # return render(request, "auctions/watchlist.html", {"message": message})
    return redirect('watchlist')

@login_required
def remove_from_watchlist(request, item_id):
    listing = get_object_or_404(AuctionListing, pk=item_id)
    watchlist = Watchlist.objects.filter(user=request.user, listing=listing)
    watchlist.delete()
    # message = "Removed from watchlist."
    return redirect('watchlist')
    # return render(request, "auctions/watchlist.html", {"message": message})