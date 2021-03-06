# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 06:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_update', models.BooleanField(default=False)),
                ('totalscore', models.IntegerField(default=0)),
                ('college', models.CharField(blank=True, max_length=255, null=True)),
                ('profileimage', models.FileField(blank=True, null=True, upload_to=b'')),
                ('dateofbirth', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('joinDate', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
