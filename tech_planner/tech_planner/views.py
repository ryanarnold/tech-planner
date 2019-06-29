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
PRODUCTS_URL = 'products'

# Templates
BUILDS_HTML = 'builds.html'
PRODUCTS_HTML = 'products.html'
CATEGORIES_HTML = 'categories.html'

def index(request):
    return HttpResponseRedirect(reverse(BUILDS_URL))


def builds(request):
    if request.method == HTTP_POST:
        build_name = request.POST.get('name')

        Build.objects.create(
            name=build_name
        )

        return HttpResponseRedirect(reverse(BUILDS_URL))
    
    builds = Build.objects.order_by('name')

    context = {
        'builds': builds
    }

    return render(request, BUILDS_HTML, context)


def build_delete(request, build_id):
    Build.objects.get(id=build_id).delete()
    return HttpResponseRedirect(reverse(BUILDS_URL))


def products(request):
    if request.method == HTTP_POST:
        product_name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')

        Product.objects.create(
            name=product_name,
            category=Category.objects.get(id=category_id),
            price=price
        )

        return HttpResponseRedirect(reverse(PRODUCTS_URL))

    products = Product.objects.order_by('category', 'name')
    categories = Category.objects.order_by('name')

    context = {
        'products': products,
        'categories': categories
    }

    # Format prices
    for product in products:
        product.price = '{:,.2f}'.format(product.price)
    

    return render(request, PRODUCTS_HTML, context)


def product_delete(request, product_id):
    Product.objects.filter(id=product_id).delete()
    return HttpResponseRedirect(reverse(PRODUCTS_URL))


def categories(request):
    if request.method == HTTP_POST:
        category_name = request.POST.get('name')

        Category.objects.create(
            name=category_name
        )

        return HttpResponseRedirect(reverse(CATEGORIES_URL))

    categories = Category.objects.order_by('name')

    context = {
        'categories': categories
    }
    
    return render(request, CATEGORIES_HTML, context)


def category_delete(request, category_id):
    Category.objects.filter(id=category_id).delete()
    return HttpResponseRedirect(reverse(CATEGORIES_URL))
