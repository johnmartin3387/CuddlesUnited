# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lostpet_auth', '0002_pet_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 14, 5, 55, 568294, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
