# Generated by Django 3.2.5 on 2023-08-27 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20230826_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='timings',
            name='delivery',
            field=models.CharField(max_length=256, null=True),
        ),
    ]