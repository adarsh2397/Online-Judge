# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 10:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0010_auto_20170401_1027'),
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
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
