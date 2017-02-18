# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lostpet_auth', '0008_client_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
            ],
            options={
                'db_table': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path_key', models.CharField(max_length=255, null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Post',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='city',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='pricing',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='stripe_uid',
            field=models.CharField(default='', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='client',
            field=models.ForeignKey(blank=True, to='lostpet_auth.Client', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, to='lostpet_auth.Post', null=True),
        ),
    ]
