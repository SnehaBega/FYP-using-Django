# Generated by Django 4.2.6 on 2024-03-23 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beadaz', '0013_replacementrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResizingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Full Name')),
                ('email', models.EmailField(max_length=100, verbose_name='Email Address')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('resizing_options', models.CharField(choices=[('rings', 'Rings Re-sizing'), ('bracelets', 'Bracelets Resizing'), ('necklace', 'Necklace Resizing')], max_length=20, verbose_name='Re-sizing Options')),
                ('street_address_1', models.CharField(max_length=100, verbose_name='Address')),
                ('pickup_location', models.CharField(choices=[('Chabahil', 'Chabahil'), ('Kapan', 'Kapan'), ('Naxal', 'Naxal'), ('Boudha', 'Boudha')], max_length=50, verbose_name='Available PickUp Location')),
                ('description', models.TextField(verbose_name='Description of resizing')),
                ('additional_details', models.TextField(verbose_name='Any additional details to resizing')),
            ],
        ),
    ]