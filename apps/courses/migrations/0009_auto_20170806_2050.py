# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-06 20:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_techer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='techer',
            new_name='teacher',
        ),
    ]
