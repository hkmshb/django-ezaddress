# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezaddress', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='altitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='gps_error',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.ForeignKey(related_name='+', null=True, blank=True, verbose_name='State', to='ezaddress.State'),
        ),
        migrations.AlterField(
            model_name='address',
            name='town_city',
            field=models.CharField(blank=True, max_length=50, verbose_name='Town/City'),
        ),
    ]
