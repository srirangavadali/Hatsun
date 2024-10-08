# Generated by Django 4.2.15 on 2024-08-07 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.SmallIntegerField()),
                ('label', models.CharField(max_length=150)),
                ('is_display', models.BooleanField(default=True, null=True)),
                ('display_order', models.SmallIntegerField()),
                ('unit_of_measure', models.CharField(blank=True, max_length=150, null=True)),
                ('max_value', models.FloatField()),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(class)s', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StatusMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True, null=True, verbose_name='Is Active')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TemperatureReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('received_at', models.DateTimeField()),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.channel')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(class)s', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(class)s', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('connection_name', models.CharField(max_length=150)),
                ('status', models.BooleanField(default=True, null=True)),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(class)s', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('updated_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(class)s', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='channel',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.device'),
        ),
        migrations.AddField(
            model_name='channel',
            name='updated_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(class)s', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('connection_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.device')),
            ],
        ),
    ]
