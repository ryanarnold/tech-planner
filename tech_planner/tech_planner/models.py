from django.db.models import (Model, ForeignKey, DecimalField, CASCADE, 
    CharField)


class Category(Model):
    name = CharField(max_length=500)


class Product(Model):
    name = CharField(max_length=500)
    category = ForeignKey(Category, on_delete=CASCADE)
    price = DecimalField(max_digits=9, decimal_places=2)


class Build(Model):
    name = CharField(max_length=500)


class BuildProduct(Model):
    status_codes = (
        ('BOUGHT', 'BOUGHT'),
        ('TO-BUY', 'TO-BUY')
    )

    build = ForeignKey(Build, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    status_code = CharField(max_length=50, choices=status_codes)
