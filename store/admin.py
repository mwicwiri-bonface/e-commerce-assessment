from django.contrib import admin
from django.contrib.admin import ModelAdmin

from core.mixins import ExportCsvMixin
from store.models import Category, Gallery, Product, OrderItem, Order, Rating


@admin.register(Category)
class CategoryAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['name']
    list_display = ['slug', 'name', 'created', 'updated']
    list_display_links = ['slug', 'name']
    search_help_text = "Search by name"
    list_filter = ('updated', 'created')
    actions = ['export_as_csv']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class GalleryInline(admin.TabularInline):
    model = Gallery


@admin.register(Product)
class ProductAdmin(ExportCsvMixin, ModelAdmin):
    inlines = [
        GalleryInline,
    ]
    search_fields = ['slug', "name"]
    list_display = ['slug', "name", "category", "price", "image", "quantity", 'created', 'updated']
    list_display_links = ['slug', 'name']
    search_help_text = "Search by name"
    list_filter = ('updated', 'created')
    actions = ['export_as_csv']

    def has_change_permission(self, request, obj=None):
        return True


@admin.register(Rating)
class RatingAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['slug', "product__name", "customer__user__username"]
    list_display = ['slug', "customer", "product", "rating", 'created', 'updated']
    list_display_links = ['slug', 'customer']
    search_help_text = "Search by product name"
    list_filter = ('updated', 'created')
    actions = ['export_as_csv']

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(ExportCsvMixin, ModelAdmin):
    inlines = [
        OrderItemInline,
    ]
    search_fields = ['slug', "user__username", "user__email", "user__first_name", "user__last_name"]
    list_display = ['slug', "user", "is_completed", "is_paid", 'created', 'updated']
    list_display_links = ['slug', 'user']
    search_help_text = "Search by name"
    list_filter = ('updated', 'created')
    actions = ['export_as_csv']

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False
