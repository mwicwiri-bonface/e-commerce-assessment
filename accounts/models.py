from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core.utils import TimeStampModel, convert_to_webp


class User(AbstractUser):
    class UserTypes(models.TextChoices):
        CUSTOMER = 'CM', _('Customer')
        # Add any other user types here

    name = models.CharField(max_length=250)
    type = models.CharField(max_length=5, choices=UserTypes.choices, default=UserTypes.CUSTOMER)
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']


class AbstractProfileModel(TimeStampModel):
    class GenderTypes(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    slug = AutoSlugField(populate_from='user.name')
    image = models.ImageField(upload_to='profiles/%Y/%m/', null=True, blank=True)
    nationality = CountryField(blank_label='select country', default="KE")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_number = PhoneNumberField(blank=True)
    gender = models.CharField(max_length=2, choices=GenderTypes.choices, default=GenderTypes.FEMALE)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = convert_to_webp(self.image)
        super(AbstractProfileModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.name

    class Meta:
        abstract = True


class Customer(AbstractProfileModel):
    pass

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
