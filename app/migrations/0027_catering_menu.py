# Generated by Django 3.2.5 on 2023-10-05 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_balance_transition_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catering_menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]
