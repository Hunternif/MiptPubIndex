# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpicore', '0002_auto_20141005_0330'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiptChair',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name_en', models.CharField(max_length=500, blank=True)),
                ('name_ru', models.CharField(max_length=500)),
                ('rank', models.IntegerField(default=0)),
                ('department', models.ForeignKey(to='mpicore.MiptDepartment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='miptdepartment',
            old_name='mipt_index',
            new_name='rank',
        ),
        migrations.RemoveField(
            model_name='author',
            name='mipt_department',
        ),
        migrations.AddField(
            model_name='author',
            name='mipt_chair',
            field=models.ForeignKey(null=True, blank=True, to='mpicore.MiptChair'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journal',
            name='issn',
            field=models.CharField(max_length=50, verbose_name='ISSN'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='rank_sjr',
            field=models.FloatField(verbose_name='SJR (SCImago Journal Rank)', default=0),
        ),
        migrations.AlterField(
            model_name='journal',
            name='rank_snip',
            field=models.FloatField(verbose_name='SNIP (Source Normalized Impact per Paper)', default=0),
        ),
        migrations.AlterField(
            model_name='miptdepartment',
            name='name_en',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='miptdepartment',
            name='name_ru',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='publication',
            name='doi',
            field=models.CharField(max_length=100, verbose_name='DOI (Digital Object Identifier)'),
        ),
    ]
