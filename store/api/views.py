from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from store.pagination import StandardResultsSetPagination
from store.selectors import get_category_list
from store.serializers import CategorySerializer


class CategoryList(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return get_category_list()
