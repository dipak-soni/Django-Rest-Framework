# Generated by Django 5.0.3 on 2024-10-02 18:56

import cardekho_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardekho_app', '0002_carlist_carnumber_carlist_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShowRoomList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=100)),
                ('website', models.URLField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='carlist',
            name='carnumber',
            field=models.CharField(blank=True, max_length=29, null=True, validators=[cardekho_app.models.alphanumeric]),
        ),
    ]
