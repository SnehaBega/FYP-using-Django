# Generated by Django 4.2.7 on 2024-04-25 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beadaz', '0018_remove_cart_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customization',
            name='length',
            field=models.CharField(max_length=50, verbose_name='length-cm'),
        ),
    ]
