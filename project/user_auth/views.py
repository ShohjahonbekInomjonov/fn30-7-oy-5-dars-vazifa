from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpRequest
from django.contrib import messages

from user_auth.forms import LoginForm, RegistrationForm

# Create your views here.

def user_login(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Authenticationdan muvaffaqqiyatli o'tdingiz😊😊😊")
            return redirect('home')
    else:
        form = LoginForm()
    
    context = {
        "form": form,
        "title": "Authentication"
    }
    return render(request, "auth/login.html", context)


def user_register(request: HttpRequest):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User muvaffaqqiyatli yaratildi😊😊😊")
            return redirect('login')
    else:
        form = RegistrationForm()
    
    context = {
        "form": form,
        "title": "Registration"
    }
    return render(request, "auth/register.html", context)


def user_logout(request: HttpRequest):
    logout(request)
    messages.success(request, "Tizimdan muvaffaqqiyatli chiqdingiz😊😊😊")
    return redirect('login')