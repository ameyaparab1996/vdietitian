# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-24 11:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dietplan', '0005_auto_20180311_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vduser',
            name='user',
        ),
        migrations.DeleteModel(
            name='VDUser',
        ),
    ]
