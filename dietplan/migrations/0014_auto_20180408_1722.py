# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-08 11:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dietplan', '0013_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='is_positive',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='feedback_on',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 8, 11, 52, 31, 996547, tzinfo=utc)),
        ),
    ]
