# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0007_auto_20170401_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_update', models.BooleanField(default=False)),
                ('totalscore', models.IntegerField(default=0)),
                ('college', models.CharField(blank=True, max_length=255, null=True)),
                ('profileimage', models.FileField(blank=True, null=True, upload_to=b'')),
                ('dateofbirth', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('joinDate', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]
