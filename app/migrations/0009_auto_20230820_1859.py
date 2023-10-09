# Generated by Django 3.2.5 on 2023-08-20 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20230820_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='services',
        ),
        migrations.AddField(
            model_name='code',
            name='amount',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='code',
            name='delfrom',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='code',
            name='delto',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='code',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='code_driver', to='app.driver'),
        ),
        migrations.AddField(
            model_name='code',
            name='timefrom',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='code',
            name='timeto',
            field=models.CharField(max_length=256, null=True),
        ),
    ]