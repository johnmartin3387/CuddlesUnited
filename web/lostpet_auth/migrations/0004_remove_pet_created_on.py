# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lostpet_auth', '0003_client_created_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='created_on',
        ),
    ]
