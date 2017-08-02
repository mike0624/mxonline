# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-29 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20170618_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_id',
            field=models.IntegerField(default=0, verbose_name='收藏id'),
        ),
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_type',
            field=models.IntegerField(choices=[(1, '课程'), (2, '课程机构'), (3, '教师')], max_length=2, verbose_name='类型'),
        ),
    ]
