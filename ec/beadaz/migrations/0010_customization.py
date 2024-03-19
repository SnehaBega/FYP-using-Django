# Generated by Django 4.2.6 on 2024-03-17 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beadaz', '0009_blog_extra_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_num', models.CharField(max_length=15)),
                ('product_type', models.CharField(max_length=100)),
                ('bead_material', models.CharField(choices=[('glass', 'Glass'), ('crystal', 'Crystal'), ('gemstone', 'Gemstone'), ('seedBeads', 'Seed Beads')], max_length=20)),
                ('bead_colour', models.CharField(max_length=100)),
                ('closure_type', models.CharField(choices=[('lobster', 'Lobster Clasp'), ('magnetic', 'Magnetic Clasp'), ('toggle', 'Toggle Clasp')], max_length=20)),
                ('length', models.CharField(max_length=50)),
                ('metal_type', models.CharField(choices=[('gold-plated', 'Gold-plated'), ('silver', 'Silver'), ('copper', 'Copper')], max_length=20)),
                ('shipping_address', models.CharField(max_length=255)),
            ],
        ),
    ]
