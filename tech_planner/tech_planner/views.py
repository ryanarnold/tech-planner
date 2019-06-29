from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# URLs
BUILDS_URL = 'builds'

# Templates
BUILDS_HTML = 'builds.html'
PRODUCTS_HTML = 'products.html'
CATEGORIES_HTML = 'categories.html'

def index(request):
    return HttpResponseRedirect(reverse(BUILDS_URL))


def builds(request):
    return render(request, BUILDS_HTML)


def products(request):
    return render(request, PRODUCTS_HTML)


def categories(request):
    return render(request, CATEGORIES_HTML)
