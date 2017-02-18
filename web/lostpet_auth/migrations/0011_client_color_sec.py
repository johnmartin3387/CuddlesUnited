# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lostpet_auth', '0010_comment_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='color_sec',
            field=models.CharField(default='', max_length=255, null=True, blank=True),
        ),
    ]
