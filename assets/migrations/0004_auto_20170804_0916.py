# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-04 01:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_auto_20170801_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardwareasset',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='organisation.Location'),
        ),
    ]