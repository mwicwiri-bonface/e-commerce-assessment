from django.db import transaction
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, \
    RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from store.models import Order
from store.selectors import get_category_list, get_product_list, get_order_list
from store.serializers import CategorySerializer, ProductSerializer, OrderSerializer, PlaceOrderSerializer


@method_decorator(swagger_auto_schema(operation_id='Add category - POST'), name='post')
class CategoryCreateAPIView(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [HasAPIKey, IsAuthenticated]

    def get_queryset(self):
        return get_category_list()


@method_decorator(swagger_auto_schema(operation_id='List categories - GET'), name='get')
class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        return get_category_list()


@method_decorator(swagger_auto_schema(operation_id='Category details - GET'), name='get')
class CategoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = CategorySerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        return get_category_list()


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [HasAPIKey, IsAuthenticated]

    def get_queryset(self):
        return get_category_list()

    @method_decorator(name='get', decorator=swagger_auto_schema(operation_id='Category details - GET'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @method_decorator(name='put', decorator=swagger_auto_schema(operation_id='Category update - PUT'))
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @method_decorator(name='patch', decorator=swagger_auto_schema(operation_id='Category partial update - PATCH'))
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @method_decorator(name='delete', decorator=swagger_auto_schema(operation_id='Category delete - DELETE'))
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@method_decorator(name='post', decorator=swagger_auto_schema(operation_id='Add Product - POST'))
class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [HasAPIKey, IsAuthenticated]

    def get_queryset(self):
        return get_product_list()


@method_decorator(name='get', decorator=swagger_auto_schema(operation_id='Product List - GET'))
class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        return get_product_list()


@method_decorator(name='get', decorator=swagger_auto_schema(operation_id='Product details - GET'))
class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [HasAPIKey]
    lookup_field = "slug"

    def get_queryset(self):
        return get_product_list()


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [HasAPIKey, IsAuthenticated]

    def get_queryset(self):
        return get_product_list()

    @method_decorator(name='get', decorator=swagger_auto_schema(operation_id='Product details - GET'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @method_decorator(name='put', decorator=swagger_auto_schema(operation_id='Product update - PUT'))
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @method_decorator(name='patch', decorator=swagger_auto_schema(operation_id='Product partial update - PATCH'))
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @method_decorator(name='delete', decorator=swagger_auto_schema(operation_id='Product delete - DELETE'))
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [HasAPIKey, IsAuthenticated]

    def get_queryset(self):
        return get_order_list(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    @method_decorator(name='get', decorator=swagger_auto_schema(operation_id='Order List - GET'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @method_decorator(name='post', decorator=swagger_auto_schema(operation_id='Endpoint to create am order - POST'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PlaceOrderAPIView(APIView):
    permission_classes = [HasAPIKey, IsAuthenticated]
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

    @method_decorator(name='post', decorator=swagger_auto_schema(operation_id='Place order - POST'))
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
