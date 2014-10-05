# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpicore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('issn', models.CharField(max_length=50)),
                ('name_en', models.CharField(max_length=200)),
                ('rank_sjr', models.FloatField(default=0)),
                ('rank_snip', models.FloatField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='publication',
            name='journal',
            field=models.ForeignKey(to='mpicore.Journal', default=''),
            preserve_default=False,
        ),
    ]
