from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

from core.utils import TimeStampModel, generate_key


class Category(TimeStampModel):
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories", blank=True)
    publish = models.BooleanField(_('Publish'), default=False, help_text=_('Publish, allow to display'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(TimeStampModel):
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=150)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', null=True, blank=True)
    image = models.ImageField(upload_to='product/images/%Y/%m/%d/', null=True)
    quantity = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish = models.BooleanField(_('Publish'), default=False, help_text=_('Publish, allow to display'))

    def __str__(self):
        return self.name


class Gallery(TimeStampModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True, related_name="gallery")
    image = models.ImageField(upload_to='product/images/%Y/%m/%d/', null=True, blank=True)
    publish = models.BooleanField(_('Publish'), default=False, help_text=_('Publish, allow to display'))

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'


class Rating(TimeStampModel):
    class Ratings(models.IntegerChoices):
        ONE_STAR = 1, _('One star')
        TWO_STAR = 2, _('Two star')
        THREE_STAR = 3, _('Three star')
        FOUR_STAR = 4, _('Four star')
        FIVE_STAR = 5, _('Five star')

    slug = AutoSlugField(populate_from='slug_name')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings")
    customer = models.ForeignKey(to="accounts.Customer", on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.ImageField(choices=Ratings.choices, default=Ratings.FIVE_STAR)

    @staticmethod
    def slug_name():
        slug = generate_key(8, 8)
        return slug


class Order(TimeStampModel):
    slug = AutoSlugField(populate_from='slug_name')
    user = models.ForeignKey(to="accounts.User", on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)

    @staticmethod
    def slug_name():
        slug = generate_key(8, 8)
        return slug

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_total()
        return total

    def get_total_quantity(self):
        total = 0
        for item in self.items.all():
            total += item.quantity
        return total

    def __str__(self):
        return f"{self.slug} : {self.user.email}"


class OrderItem(TimeStampModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_rated = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

    def get_total(self):
        total = self.product.price * self.quantity
        return total
