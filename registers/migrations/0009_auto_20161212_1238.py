# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-12 04:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0003_computer_location'),
        ('registers', '0008_auto_20161028_1610'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='backup',
            options={'ordering': ('computer__hostname',)},
        ),
        migrations.RemoveField(
            model_name='itsystem',
            name='softwares',
        ),
        migrations.AddField(
            model_name='backup',
            name='computer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tracking.Computer'),
        ),
        migrations.AddField(
            model_name='itsystemhardware',
            name='computer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tracking.Computer'),
        ),
    ]
