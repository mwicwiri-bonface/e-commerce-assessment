from django.urls import path

from store.api.views import CategoryList

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list')
]
