# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-03 01:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0017_location_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='costcentre',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]