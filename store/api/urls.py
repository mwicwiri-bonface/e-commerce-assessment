from django.urls import path

from store.api.views import CategoryRetrieveUpdateDestroyAPIView, ProductListAPIView, ProductCreateAPIView, \
    CategoryRetrieveAPIView, ProductRetrieveAPIView, ProductRetrieveUpdateDestroyAPIView, CategoryCreateAPIView, \
    CategoryListAPIView, OrderListCreateAPIView

urlpatterns = [
    path('add-category/', CategoryCreateAPIView.as_view()),
    path('categories/', CategoryListAPIView.as_view()),
    path('categories/<str:slug>/', CategoryRetrieveUpdateDestroyAPIView.as_view()),
    path('category-detail/<str:slug>/', CategoryRetrieveAPIView.as_view()),
    path('products/', ProductListAPIView.as_view()),
    path('add-product/', ProductCreateAPIView.as_view()),
    path('products/<str:slug>/', ProductRetrieveUpdateDestroyAPIView.as_view()),
    path('product-detail/<str:slug>/', ProductRetrieveAPIView.as_view()),
    path('orders/', OrderListCreateAPIView.as_view()),
]
