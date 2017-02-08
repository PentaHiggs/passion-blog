# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='categories',
            field=models.ManyToManyField(to='blog.BlogPostCategory', blank=True),
            preserve_default=True,
        ),
    ]
