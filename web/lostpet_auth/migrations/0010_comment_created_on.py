# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lostpet_auth', '0009_auto_20170120_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 21, 1, 2, 43, 853258, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
