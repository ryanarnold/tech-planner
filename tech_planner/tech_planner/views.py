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
PRODUCT_EDIT_HTML = 'product_edit.html'
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
    build_products = BuildProduct.objects.filter(build=build)
    build_products = build_products.order_by('product__category__name', 'product__name')

    # Get total price when complete
    total_price_num = sum([x.product.price for x in build_products])
    total_price = format_as_currency(total_price_num)
    
    # Get total price currently
    current_price_num = sum([x.product.price for x in build_products if x.status_code == 'BOUGHT'])
    current_price = format_as_currency(current_price_num)

    # Get cost balance
    cost_balance_num = total_price_num - current_price_num
    cost_balance = format_as_currency(cost_balance_num)

    context = {
        'build': build,
        'categories': categories,
        'build_products': build_products,
        'total_price': total_price,
        'current_price': current_price,
        'cost_balance': cost_balance,
    }
    
    for build_product in build_products:
        price = build_product.product.price

        if price == 0:
            build_product.product.price = '--'
        else:
            build_product.product.price = format_as_currency(
                build_product.product.price)

    return render(request, BUILD_EDIT_HTML, context)


def build_edit_name(request, build_id):
    if request.method == HTTP_POST:
        new_build_name = request.POST.get('name')

        build = Build.objects.get(id=build_id)
        build.name = new_build_name

        build.save()

        return HttpResponseRedirect(reverse(BUILD_EDIT_URL, args=(build_id,)))


def build_product_update_status(request, build_product_id, status):
    build_product = BuildProduct.objects.get(id=build_product_id)
    build_product.status_code = status
    build_product.save()

    print(build_product.status_code)

    return HttpResponseRedirect(reverse(BUILD_EDIT_URL, args=(build_product.build.id,)))


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

    products = Product.objects.order_by('category__name', 'name')
    categories = Category.objects.order_by('name')

    context = {
        'products': products,
        'categories': categories
    }

    for product in products:
        if product.price == 0:
            product.price = '--'
        else:
            product.price = format_as_currency(product.price)

    return render(request, PRODUCTS_HTML, context)


def product_edit(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == HTTP_POST:
        new_product_name = request.POST.get('name')
        new_category = Category.objects.get(id=request.POST.get('category'))
        new_price = request.POST.get('price')

        product.name = new_product_name
        product.category = new_category
        product.price = new_price

        product.save()

        return HttpResponseRedirect(reverse('products'))

    categories = Category.objects.order_by('name')

    context = {
        'product': product,
        'categories': categories
    }

    return render(request, PRODUCT_EDIT_HTML, context)


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
