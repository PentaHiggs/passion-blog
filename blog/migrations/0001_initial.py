# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField()),
                ('post_body', models.TextField()),
                ('author', models.ForeignKey(to='blog.Author')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField()),
                ('post_body', models.TextField()),
                ('author', models.ForeignKey(to='blog.Author')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogPostCategory',
            fields=[
                ('category_name', models.CharField(max_length=20, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='categories',
            field=models.ManyToManyField(to='blog.BlogPostCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='parent_blog_post',
            field=models.ForeignKey(to='blog.BlogPost'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='response_to',
            field=models.ForeignKey(to='blog.BlogComment', blank=True),
            preserve_default=True,
        ),
    ]
