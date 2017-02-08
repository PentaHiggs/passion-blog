# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20141113_0115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='categories',
        ),
    ]
