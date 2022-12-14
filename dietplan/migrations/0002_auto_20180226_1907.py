# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-26 13:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dietplan', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='food_prefernce',
        ),
        migrations.AddField(
            model_name='userdetails',
            name='food_preference',
            field=models.CharField(choices=[('V', 'Veg'), ('NV', 'Non-veg'), ('VE', 'Veg including Egg')], default='NV', max_length=20),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='date_of_birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=6),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='goal',
            field=models.CharField(choices=[('GW', 'Gain weight'), ('LW', 'Loose weight'), ('SF', 'Stay Fit')], default='LW', max_length=2),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='lifestyle',
            field=models.CharField(choices=[('S', 'Sedentary'), ('LA', 'Lightly active'), ('MA', 'Moderately active'), ('VA', 'Very active'), ('EA', 'Extremely active')], default='MA', max_length=2),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='medical_history',
            field=models.CharField(choices=[('D', 'Diabities'), ('HT', 'Hypothyroidism'), ('None', 'None')], default='None', max_length=4),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='profession',
            field=models.CharField(choices=[('ST', 'Student'), ('GIFW', 'Graduate/Intern/Fresher Job/Work from Home'), ('CW', 'Corporate Work'), ('MEG', 'Medical/Education/Governmental work'), ('PLW', 'Physical Labour Work')], default='ST', max_length=4),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
