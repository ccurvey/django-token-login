# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0003_auto_20150902_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='merged_token',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='secret_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
