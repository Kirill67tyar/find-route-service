# Generated by Django 3.2.9 on 2022-04-13 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0002_alter_city_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.CharField(max_length=50)),
                ('b', models.CharField(max_length=50)),
            ],
        ),
    ]
