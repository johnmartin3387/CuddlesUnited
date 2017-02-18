# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lostpet_auth', '0005_auto_20161226_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='verified_email',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
