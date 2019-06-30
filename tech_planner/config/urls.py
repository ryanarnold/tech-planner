"""tech_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tech_planner import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    # Builds
    path('builds/', views.builds, name='builds'),
    path('build-delete/<int:build_id>/', views.build_delete, name='build_delete'),
    path('build-product-delete/<int:build_product_id>/', views.build_product_delete, name='build_product_delete'),
    path('build-edit/<int:build_id>/', views.build_edit, name='build_edit'),

    # Categories
    path('categories/', views.categories, name='categories'),
    path('category-delete/<int:category_id>/', views.category_delete, name='category_delete'),

    # Products
    path('products/', views.products, name='products'),
    path('product-delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('get-products-using-category/<int:category_id>/', views.get_products, name='get-products'),
]
