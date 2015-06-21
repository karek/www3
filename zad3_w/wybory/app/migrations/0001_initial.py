# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gmina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazwa', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Obwod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adres', models.CharField(max_length=200)),
                ('uprawnionych', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('ileKart', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('gmina', models.ForeignKey(to='app.Gmina')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
