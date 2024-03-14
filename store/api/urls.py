from django.urls import path
from rest_framework.generics import ListCreateAPIView

from store.api.views import CategoryRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('categories/', ListCreateAPIView.as_view()),
    path('categories/<str:slug>/', CategoryRetrieveUpdateDestroyAPIView.as_view()),
]
