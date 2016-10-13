# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-13 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registers', '0004_itsystem_backup_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itsystem',
            name='system_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Web application'), (2, 'Client application'), (3, 'Mobile application'), (4, 'Service'), (5, 'Externally hosted application')], null=True),
        ),
    ]
