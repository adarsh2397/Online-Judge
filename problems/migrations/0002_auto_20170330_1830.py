# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subs_code',
        ),
        migrations.AlterField(
            model_name='runs',
            name='tid',
            field=models.IntegerField(),
        ),
    ]
