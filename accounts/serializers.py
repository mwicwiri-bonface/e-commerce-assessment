from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

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


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'name')
        extra_kwargs = {
            'name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                name=validated_data['name']
            )

            user.set_password(validated_data['password'])
            user.save()
        return user
