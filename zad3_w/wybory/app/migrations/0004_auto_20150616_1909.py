# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150514_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gmina',
            name='wersja',
        ),
        migrations.AddField(
            model_name='obwod',
            name='wersja',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
