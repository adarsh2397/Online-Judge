# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 08:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170401_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='joinDate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
