# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-04 20:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='视频链接'),
        ),
    ]
