# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lostpet_auth', '0007_client_pet_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='password',
            field=models.CharField(default='', max_length=255, null=True, blank=True),
        ),
    ]
