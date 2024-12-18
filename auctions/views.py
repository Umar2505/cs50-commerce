from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bids, Comments


class Lists(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}))
    price = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Price' , 'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Description', 'type': 'textarea', 'class': 'form-control'}))
    img = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Image URL', 'class': 'form-control'}), required=False)
    category = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Category', 'class': 'form-control'}), required=False)

class MakeABid(forms.Form):
    price = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Price', 'class': 'form-control'}), label="")

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.exclude(inactive=True)
    })

def closed(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.exclude(inactive=False),
        "closed": True
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
    return render(request, "auctions/category.html", {
        "categories": Listing.objects.values_list("category", flat=True).distinct()
    })

def cats(request, cat):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category = cat),
        "cat": cat
    })

def lists(request, list_id):
    yours = False
    watch = False
    try:
        list = Listing.objects.get(id=list_id)
    except Listing.DoesNotExist:
        raise Http404("List not found.")
    
    try:
        ba = Bids.objects.get(price = list.price)
    except:
        pass
    else:
        if ba.bidder == request.user:
            yours = True
    if request.method == "POST":
        if "comment" in request.POST:
            c = Comments()
            c.author = request.user
            c.listing = list
            c.text = request.POST["text"]
            c.save()
            return HttpResponseRedirect(reverse("list", args=(list_id,)))
        if "close" in request.POST:
            list.inactive = True
            list.save()
            return HttpResponseRedirect(reverse("list", args=(list_id,)))
        if "watchlist" in request.POST:
            user = request.user
            if list.watchlist.filter(id=user.id).exists():
                list.watchlist.remove(user)
                watch = False
            else:
                list.watchlist.set([user])
                watch = True
        if "bid_on" in request.POST:
            bid = MakeABid(request.POST)
            if bid.is_valid():
                if bid.cleaned_data["price"] <= list.price:
                    return render(request, "auctions/list.html", {
                        "list": Listing.objects.get(id=list_id),
                        "bids": len(list.bids.all()),
                        "prince": True,
                        "form": MakeABid,
                        "yours": yours,
                        "inactive": list.inactive,
                        "comments": list.comments.all()
                    })
                else:
                    list.price = bid.cleaned_data["price"]
                    list.save()
                    b = Bids()
                    b.bidder = request.user
                    b.listing = list
                    b.price = bid.cleaned_data["price"]
                    b.save()
                    return HttpResponseRedirect(reverse("list", args=(list_id,)))
    if list.owner == request.user:     
        return render(request, "auctions/list.html", {
            "list": Listing.objects.get(id=list_id),
            "bids": list.bids.all(),
            "no_bids": True,
            "form": MakeABid,
            "yours": yours,
            "inactive": list.inactive,
            "len": len(list.bids.all()),
            "comments": list.comments.all()
        })
    user = request.user
    if list.watchlist.filter(id=user.id).exists():
        watch = True
    return render(request, "auctions/list.html", {
        "list": Listing.objects.get(id=list_id),
        "bids": len(list.bids.all()),
        "form": MakeABid,
        "prince": False,
        "yours": yours,
        "watch": watch,
        "inactive": list.inactive,
        "comments": list.comments.all()
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
            l.category = form.cleaned_data['category']
            if form.cleaned_data['img']:
                l.img = form.cleaned_data['img']
            l.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/add.html", {
        "form": Lists
    })

def watchlist(request):
    user = request.user
    return render(request, "auctions/index.html", {
        "listings": user.watchlist.all(),
        "watch": True
    })