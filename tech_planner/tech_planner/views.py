from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .common import format_as_currency
from .models import Category, Product, Build, BuildProduct

# Misc Constants
HTTP_POST = 'POST'

# URLs
BUILDS_URL = 'builds'
BUILD_EDIT_URL = 'build_edit'
CATEGORIES_URL = 'categories'
PRODUCTS_URL = 'products'

# Templates
BUILDS_HTML = 'builds.html'
BUILD_EDIT_HTML = 'build_edit.html'
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


def build_edit(request, build_id):
    build = Build.objects.get(id=build_id)

    if request.method == HTTP_POST:
        product = Product.objects.get(id=request.POST.get('product'))

        BuildProduct.objects.create(
            build=build,
            product=product,
            status_code='TO-BUY'
        )

        return HttpResponseRedirect(reverse(BUILD_EDIT_URL, args=(build_id,)))

    categories = Category.objects.order_by('name')
    products = Product.objects.order_by('name')
    build_products = BuildProduct.objects.filter(build=build)

    # Get total price
    total_price = sum([x.product.price for x in build_products])
    total_price = format_as_currency(total_price)

    context = {
        'build': build,
        'categories': categories,
        'products': products,
        'build_products': build_products,
        'total_price': total_price
    }
    
    for build_product in build_products:
        build_product.product.price = format_as_currency(
            build_product.product.price)

    return render(request, BUILD_EDIT_HTML, context)


def build_product_delete(request, build_product_id):
    build_product = BuildProduct.objects.get(id=build_product_id)
    build_id = build_product.build.id
    build_product.delete()

    return HttpResponseRedirect(reverse(BUILD_EDIT_URL, args=(build_id,)))


def build_delete(request, build_id):
    Build.objects.get(id=build_id).delete()

    return HttpResponseRedirect(reverse(BUILDS_URL))


def products(request):
    if request.method == HTTP_POST:
        product_name = request.POST.get('name')
        category = Category.objects.get(id=request.POST.get('category'))
        price = request.POST.get('price')

        Product.objects.create(
            name=product_name,
            category=category,
            price=price
        )

        return HttpResponseRedirect(reverse(PRODUCTS_URL))

    products = Product.objects.order_by('category', 'name')
    categories = Category.objects.order_by('name')

    context = {
        'products': products,
        'categories': categories
    }

    for product in products:
        product.price = format_as_currency(product.price)

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


def get_products(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category).order_by('name')

    products_json = [
        {
            'id': product.id,
            'name': product.name
        } 
        for product in products
    ]

    return JsonResponse(products_json, safe=False)
