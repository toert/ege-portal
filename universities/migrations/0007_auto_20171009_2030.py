# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0006_auto_20171009_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='places',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
