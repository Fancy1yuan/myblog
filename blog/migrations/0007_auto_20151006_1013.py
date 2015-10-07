# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20151006_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(max_length=5120, upload_to=b'article/%Y/%m', null=True, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe9\xa2\x98\xe5\x9b\xbe', blank=True),
            preserve_default=True,
        ),
    ]
