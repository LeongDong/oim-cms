# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-09 04:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0006_auto_20161104_1011'),
        ('tracking', '0002_auto_20161110_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='location',
            field=models.ForeignKey(blank=True, help_text='Physical location', null=True, on_delete=django.db.models.deletion.PROTECT, to='organisation.Location'),
        ),
    ]