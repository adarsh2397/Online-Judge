# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 10:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_auto_20170401_0936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='id',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='user_id',
        ),
        migrations.AddField(
            model_name='userdetails',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
