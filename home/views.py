from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    # return HttpResponse("<h1>candies.dev</h1>")
    return render(request, "home/index.html")
