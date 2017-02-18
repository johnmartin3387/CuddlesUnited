# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lostpet_auth', '0006_client_verified_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='pet_image',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
