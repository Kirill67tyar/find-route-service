# Generated by Django 3.2.9 on 2021-12-01 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities', '0002_alter_city_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название поезда')),
                ('travel_time', models.PositiveSmallIntegerField(verbose_name='Время в пути')),
                ('departure_time', models.DateTimeField(verbose_name='Время отправления')),
                ('arrival_time', models.DateTimeField(verbose_name='Время прибытия')),
                ('from_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trains_start', to='cities.city', verbose_name='Из какого города')),
                ('to_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trains_arrive', to='cities.city', verbose_name='В какой город')),
            ],
            options={
                'verbose_name': 'Поезд',
                'verbose_name_plural': 'Поезда',
                'ordering': ('travel_time',),
            },
        ),
    ]