# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(default=b'article/default.png', upload_to=b'', max_length=5120, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe9\xa2\x98\xe5\x9b\xbe'),
            preserve_default=True,
        ),
    ]
