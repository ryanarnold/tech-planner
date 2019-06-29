from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Category, Product, Build, BuildProduct

# Misc Constants
HTTP_POST = 'POST'

# URLs
BUILDS_URL = 'builds'
CATEGORIES_URL = 'categories'

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
    if request.method == HTTP_POST:
        category_name = request.POST.get('name')

        category = Category.objects.create(
            name=category_name
        )

        return HttpResponseRedirect(reverse(CATEGORIES_URL))

    categories = Category.objects.order_by('name')

    context = {
        'categories': categories
    }
    
    return render(request, CATEGORIES_HTML, context)
