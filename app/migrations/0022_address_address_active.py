# Generated by Django 3.2.5 on 2023-09-17 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20230916_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_active',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]