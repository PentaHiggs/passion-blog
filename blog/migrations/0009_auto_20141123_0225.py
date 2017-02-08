# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20141120_1446'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='blogpost',
            unique_together=set([('pub_date', 'post_title')]),
        ),
    ]
