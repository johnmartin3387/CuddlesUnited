# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lostpet_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 6, 17, 41, 597450, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
