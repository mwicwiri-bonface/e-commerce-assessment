from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, \
    RetrieveAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from store.models import Order
from store.selectors import get_category_list, get_product_list, get_order_list
from store.serializers import CategorySerializer, ProductSerializer, OrderSerializer, PlaceOrderSerializer


class CategoryCreateAPIView(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_category_list()


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return get_category_list()


class CategoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return get_category_list()


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_category_list()


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_product_list()


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return get_product_list()


class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return get_product_list()


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_product_list()


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_order_list(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class PlaceOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaceOrderSerializer

    def get_queryset(self):
        return get_order_list(user_id=self.request.user.id)

    @staticmethod
    def update_product_quantities(order):
        for item in order.items.select_for_update():
            product = item.product
            if product.quantity < item.quantity:
                raise ValueError(f"Not enough quantity available for {product.name}")
            product.quantity -= item.quantity
            product.save()

    @staticmethod
    def handle_quantity_error(order, error_message):
        with transaction.atomic():
            for item in order.items.all():
                product = item.product
                product.quantity += item.quantity
                product.save()
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            try:
                with transaction.atomic():
                    self.update_product_quantities(order)
                    order.is_completed = True
                    order.save()
            except ValueError as e:
                return self.handle_quantity_error(order, str(e))
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
