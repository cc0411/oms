# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-17 11:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salt', '0002_auto_20181017_1135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='minionlist',
            old_name='memery',
            new_name='memory',
        ),
    ]
