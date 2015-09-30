# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150929_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.CharField(default=b'nothing,', max_length=200, verbose_name=b'\xe4\xb8\xaa\xe4\xba\xba\xe7\xae\x80\xe4\xbb\x8b'),
            preserve_default=True,
        ),
    ]
