# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_blogpost_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='categories',
            field=models.ManyToManyField(to='blog.BlogPostCategory', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='response_to',
            field=models.ForeignKey(blank=True, to='blog.BlogComment', null=True),
            preserve_default=True,
        ),
    ]
