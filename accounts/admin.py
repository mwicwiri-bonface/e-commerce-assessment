from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import ngettext
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.forms import RegistrationForm, UserAdminChangeForm
from accounts.models import Customer
from core.mixins import ExportCsvMixin

User = get_user_model()

admin.site.site_header = "E-commerce Admin"
admin.site.site_title = "E-commerce Admin Portal"
admin.site.index_title = "Welcome to E-commerce  Admin Portal"

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(ExportCsvMixin, BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = RegistrationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'email', 'username', 'type')
    search_fields = ('name', 'email', 'username',)
    list_filter = ('is_active', 'updated', 'created', 'type')
    actions = ['make_active', 'make_inactive', 'export_as_csv']

    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info', {'fields': ('name', 'email', 'username')}),
        ('Permissions', {'fields': ('type',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'username', 'type', 'password1', 'password2')}
         ),
    )
    ordering = ['email']
    filter_horizontal = ()

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        messages.success(request, ngettext(
            '%d User has successfully been marked as active.',
            '%d Users have been successfully marked as active.',
            updated,
        ) % updated)

    make_active.short_description = "Activate User"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        messages.info(request, ngettext(
            '%d User has been deactivated successfully.',
            '%d Users have been deactivated successfully.',
            updated,
        ) % updated)

    make_inactive.short_description = "Archive User"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


@admin.register(Customer)
class ProfileAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['user__name']
    list_display = ['user']
    list_display_links = ['user']
    search_help_text = "Search by name"
    list_filter = ('updated', 'created')
    actions = ['export_as_csv']

    def has_change_permission(self, request, obj=None):
        return True
