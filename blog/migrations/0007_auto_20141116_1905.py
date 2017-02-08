# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20141116_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='post_title',
            field=models.CharField(default=b'', max_length=101, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='post_title',
            field=models.CharField(default=b'', max_length=101, blank=True),
            preserve_default=True,
        ),
    ]
