# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-02 03:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ers_admin', '0002_client_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='create_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='client',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.IntegerField(default=0, help_text='\u7ec8\u7aef\u63a5\u5165\u72b6\u6001: 0: \u672a\u6fc0\u6d3b\uff0c 1: \u6b63\u5e38'),
        ),
    ]
