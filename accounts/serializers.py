from django.contrib.auth import get_user_model
from django_countries.serializers import CountryFieldMixin
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from accounts.models import Customer

User = get_user_model()


class UserSimpleSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active']


class CustomerSerializer(CountryFieldMixin, ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['user']


class UserSerializer(CountryFieldMixin, ModelSerializer):
    profile_info = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'profile_info']
        ref_name = 'AccountsUser'

    @staticmethod
    def get_profile_info(obj):
        profile, _ = Customer.objects.get_or_create(user=obj)
        return CustomerSerializer(profile).data
