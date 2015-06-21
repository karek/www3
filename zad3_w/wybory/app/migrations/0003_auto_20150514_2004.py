# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_obwod_wersja'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='obwod',
            name='wersja',
        ),
        migrations.AddField(
            model_name='gmina',
            name='wersja',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
