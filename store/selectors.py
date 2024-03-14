from typing import Optional

from django.db.models import QuerySet

from store.models import Category, Product, Rating, Order


def get_category_list(display: Optional[bool] = None) -> QuerySet[Category]:
    queryset = Category.objects.all()
    if display:
        queryset = queryset.filter(display=display)
    return queryset


def get_product_list(display: Optional[bool] = None) -> QuerySet[Product]:
    queryset = Product.objects.select_related('category').all()
    if display:
        queryset = queryset.filter(display=display)
    return queryset


def get_rating_list() -> QuerySet[Rating]:
    queryset = Rating.objects.select_related('product', 'customer').all()
    return queryset


def get_order_list(user_id: Optional[int] = None) -> QuerySet[Order]:
    queryset = Order.objects.prefetch_related('items').all()
    if user_id:
        queryset = queryset.filter(user_id=user_id)
    return queryset
