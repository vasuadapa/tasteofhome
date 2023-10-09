# Generated by Django 3.2.5 on 2023-10-06 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_catering_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_address_customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_code', to='app.code'),
        ),
    ]
