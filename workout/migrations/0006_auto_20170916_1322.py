# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-16 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0005_auto_20170916_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyweight',
            name='weight',
            field=models.FloatField(help_text='Weight in kg'),
        ),
    ]
