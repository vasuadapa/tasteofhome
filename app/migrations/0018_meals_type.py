# Generated by Django 3.2.5 on 2023-09-16 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_rename_user_user_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='meals',
            name='type',
            field=models.CharField(default='meals', max_length=256, null=True),
        ),
    ]
