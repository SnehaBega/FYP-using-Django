# Generated by Django 4.2.6 on 2024-03-05 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beadaz', '0008_blog_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='extra_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]