# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='desc',
            field=models.CharField(max_length=400, verbose_name='课程描述'),
        ),
    ]