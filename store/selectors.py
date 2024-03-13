from typing import Optional

from django.db.models import QuerySet

from store.models import Category, Product, Rating, Order


def get_category_list(display: Optional[bool] = None) -> QuerySet[Category]:
    queryset = Category.objects.all()
    if display:
        queryset = queryset.filter(display=display)
    return queryset


def get_product_list(display: Optional[bool] = None) -> QuerySet[Product]:
    queryset = Product.objects.all()
    if display:
        queryset = queryset.filter(display=display)
    return queryset


def get_rating_list() -> QuerySet[Rating]:
    queryset = Rating.objects.all()
    return queryset


def get_order_list() -> QuerySet[Order]:
    queryset = Order.objects.all()
    return queryset
