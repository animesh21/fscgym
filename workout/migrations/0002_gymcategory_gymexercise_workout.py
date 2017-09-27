# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-14 12:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workout', '0001_squashed_0014_auto_20170914_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='GymCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='uploads/gym_categories/')),
            ],
        ),
        migrations.CreateModel(
            name='GymExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('image', models.ImageField(upload_to='uploads/gym_exercises/')),
                ('default_timeout', models.DurationField(blank=True)),
                ('gym_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.GymCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeout', models.DurationField(blank=True)),
                ('sets', models.IntegerField()),
                ('reps', models.IntegerField()),
                ('gym_exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.GymExercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
