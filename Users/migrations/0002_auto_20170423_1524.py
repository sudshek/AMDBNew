# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='contact',
            field=models.IntegerField(default=0),
        ),
    ]