# Generated by Django 3.2.5 on 2023-09-16 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_order_subscriber_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(default='Not Paid', max_length=256, null=True),
        ),
    ]