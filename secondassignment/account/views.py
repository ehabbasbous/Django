from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def signup(request):

    error = None
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if not (name and email and password):
            error = "Please fill all fields."
        else:
            if User.objects.filter(username=email).exists():
                error = "A user with that email already exists."
            else:
                try:
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        first_name=name
                    )
                    user.save()
                    return redirect('account:login')
                except IntegrityError:
                    error = "Could not create user. Try again."

    return render(request, 'account/signup.html', {"error": error})


def login_user(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('account:dashboard')
        else:
            error = "Incorrect email or password."

    return render(request, 'account/login.html', {"error": error})


@login_required(login_url='account:login')
def dashboard(request):
    name = request.user.first_name or request.user.username
    return render(request, 'account/dashboard.html', {"name": name})


def logout_user(request):
    logout(request)
    return redirect('account:login')
