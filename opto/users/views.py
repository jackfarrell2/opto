from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User
from django.db import IntegrityError


def index(request):
    """Home page"""
    return render(request, 'users/index.html')


def login_view(request):
    """Offer login functionality"""
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "users/login.html")


def logout_view(request):
    """Offer logout functionality"""
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register_view(request):
    """Offer register functionality"""
    if request.method == "POST":
        # Gather user info
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "users/register.html",
                          {"message": "Passwords must match."})
        # Attempt to create a new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "users/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))  # Homepage redirect
    else:
        return render(request, "users/register.html")
