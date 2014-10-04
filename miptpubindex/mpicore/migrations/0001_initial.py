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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('author_id', models.CharField(max_length=50)),
                ('name_en', models.CharField(max_length=200)),
                ('name_ru', models.CharField(max_length=200)),
                ('h_index', models.IntegerField(default=0)),
                ('institute', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MiptDepartment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name_en', models.CharField(max_length=200)),
                ('name_ru', models.CharField(max_length=200)),
                ('mipt_index', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateField()),
                ('name_en', models.CharField(max_length=200)),
                ('name_ru', models.CharField(max_length=200)),
                ('doi', models.CharField(verbose_name='Digital Object Identifier', max_length=100)),
                ('citations', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='author',
            name='mipt_department',
            field=models.ForeignKey(to='mpicore.MiptDepartment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='publication',
            field=models.ForeignKey(to='mpicore.Publication'),
            preserve_default=True,
        ),
    ]
