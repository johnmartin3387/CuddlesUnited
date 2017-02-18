# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('email', models.CharField(max_length=255, null=True, blank=True)),
                ('pet_name', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('size', models.CharField(max_length=255, null=True, blank=True)),
                ('breed', models.CharField(max_length=255, null=True, blank=True)),
                ('color', models.CharField(default='', max_length=255, null=True, blank=True)),
                ('sex', models.CharField(max_length=255, null=True, blank=True)),
                ('date', models.DateTimeField()),
                ('state', models.CharField(max_length=255, null=True, blank=True)),
                ('zip_code', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'Client',
            },
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255, null=True, blank=True)),
                ('client', models.ForeignKey(blank=True, to='lostpet_auth.Client', null=True)),
            ],
            options={
                'db_table': 'Pet',
            },
        ),
    ]
