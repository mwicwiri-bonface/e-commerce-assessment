from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserSerializer
from store.models import Category, Gallery, Product, Rating, OrderItem, Order


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'name', 'image', 'publish', 'created', 'updated']


class GallerySerializer(ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'image', 'publish', 'created', 'updated']


class ProductSerializer(ModelSerializer):
    gallery = GallerySerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'image', 'publish', 'gallery', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated', 'publish']

    def create(self, validated_data):
        gallery = validated_data.pop('gallery', [])
        product = Product.objects.create(**validated_data)
        if gallery:
            Gallery.objects.bulk_create(
                [Gallery(product=product, **gallery_object)
                 for gallery_object in gallery])
        return product

    def update(self, instance, validated_data):
        gallery = validated_data.pop('gallery', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if gallery:
            Gallery.objects.bulk_create(
                [Gallery(product=instance, **gallery_object)
                 for gallery_object in gallery])
            return instance


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['slug', 'product', 'customer', 'comment', 'rating', 'created', 'updated']


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'order', 'quantity', 'is_rated', 'created', 'updated']


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['slug', 'user', 'items', 'is_completed', 'created', 'updated']
