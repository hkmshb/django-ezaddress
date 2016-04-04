# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('street', models.CharField(blank=True, verbose_name='Street Address', max_length=100)),
                ('town_city', models.CharField(blank=True, verbose_name='Town or City', max_length=50)),
                ('postal_code', models.CharField(blank=True, max_length=10)),
                ('raw', models.CharField(max_length=200)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
                'ordering': ('state', 'town_city', 'postal_code', 'street'),
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('code', models.CharField(blank=True, max_length=3)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(blank=True, max_length=3)),
                ('country', models.ForeignKey(to='ezaddress.Country', related_name='states')),
            ],
            options={
                'ordering': ('country', 'name'),
            },
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.ForeignKey(related_name='addresses', null=True, blank=True, to='ezaddress.State'),
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together=set([('name', 'country')]),
        ),
    ]
