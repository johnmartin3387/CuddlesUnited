# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lostpet_auth', '0004_remove_pet_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='collor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='client',
            name='description',
            field=models.TextField(default='', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='microchip',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='client',
            name='mixed',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
