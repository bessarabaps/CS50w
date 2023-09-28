from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from item.models import Category, Item


def index(request):
    
    Items = Item.objects.filter(active=True).all()
    return render(request, "auctions/index.html", {
        'Items': Items
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "Categories": Category.objects.all()
    })    

def category_items(request, category):
    catid = Category.objects.get(name = category)
    return render(request, "auctions/index.html", {
        "Items": Item.objects.filter(category=catid.id, active=True).all(),
        "Category": Category.objects.get(id=catid.id)
    })

def watchlist(request):
    current_user = request.user
    Items = current_user.User_watchlist.all()
    return render(request, "auctions/index.html", {
        'Items': Items
    })


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
