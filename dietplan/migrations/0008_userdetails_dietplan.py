# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-26 15:11
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dietplan', '0007_auto_20180326_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='dietPlan',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
