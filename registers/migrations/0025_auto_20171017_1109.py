# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-17 03:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registers', '0024_itsystemhardware_aws_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itsystemhardware',
            name='computer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tracking.Computer'),
        ),
    ]