# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-06 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dietplan', '0011_auto_20180404_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='BMR',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='calorieintake',
            field=models.FloatField(default=0),
        ),
    ]
