from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bids


class Lists(forms.Form):
    title = forms.CharField(max_length=200)
    price = forms.FloatField()
    description = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

def categories(request):
    pass

def lists(request, list_id):
    try:
        list = Listing.objects.get(id=list_id)
    except Listing.DoesNotExist:
        raise Http404("List not found.")
    return render(request, "auctions/list.html", {
        "list": Listing.objects.get(id=list_id),
        "bids": list.bids.all()
    })

def add(request):
    if request.method == "POST":
        user = request.user
        form = Lists(request.POST)
        if form.is_valid():
            l = Listing()
            l.owner = user
            l.title = form.cleaned_data['title']
            l.description = form.cleaned_data['description']
            l.price = form.cleaned_data['price']
            l.save()
    return render(request, "auctions/add.html", {
        "form": Lists
    })