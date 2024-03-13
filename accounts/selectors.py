from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from accounts.models import Customer

User = get_user_model()


def get_user_list(is_active: Optional[bool] = None) -> QuerySet[User]:
    queryset = User.objects.all()
    if is_active:
        queryset = queryset.filter(is_active=is_active)
    return queryset


def get_customer_list() -> QuerySet[Customer]:
    queryset = Customer.objects.select_related('user').all()
    return queryset
