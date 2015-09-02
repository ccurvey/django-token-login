# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0002_auto_20150902_1405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='logn_token_expires',
            new_name='login_token_expires',
        ),
    ]
