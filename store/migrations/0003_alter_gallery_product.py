# Generated by Django 5.0.3 on 2024-03-14 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_category_publish_remove_gallery_publish_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='store.product'),
        ),
    ]