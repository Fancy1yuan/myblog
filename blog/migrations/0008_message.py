# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20151006_1013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe7\xa7\xb0\xe5\x91\xbc')),
                ('email', models.EmailField(max_length=75, verbose_name=b'\xe9\x82\xae\xe7\xae\xb1')),
                ('message', models.TextField(verbose_name=b'\xe7\x95\x99\xe8\xa8\x80')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe7\x95\x99\xe8\xa8\x80\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u7559\u8a00',
                'verbose_name_plural': '\u7559\u8a00',
            },
            bases=(models.Model,),
        ),
    ]
