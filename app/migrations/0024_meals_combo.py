# Generated by Django 3.2.5 on 2023-10-01 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_user_data_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='meals',
            name='combo',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
