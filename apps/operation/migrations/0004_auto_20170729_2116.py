# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-29 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_auto_20170729_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_type',
            field=models.IntegerField(choices=[(1, '课程'), (2, '课程机构'), (3, '教师')], verbose_name='类型'),
        ),
    ]
