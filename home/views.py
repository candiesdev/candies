from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate


# Create your views here.

def index(request):
    prev = reverse(index, current_app="candies")
    if request.user.is_authenticated:
        sessionMenuLink = "/usr?action=logout&prev=" + prev
        sessionMenuText = "Salir"
    else:
        sessionMenuLink = "/usr?action=login&prev=" + prev
        sessionMenuText = "Autenticar"
    return render(request, "home/index.html", {
        "sessionMenuText" : sessionMenuText,
        "sessionMenuLink" : sessionMenuLink})
