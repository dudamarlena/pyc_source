# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/content/migrations/0005_content_instant_article.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 413 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('content', '0004_auto_20151103_1358')]
    operations = [
     migrations.AddField(model_name='content', name='instant_article', field=models.BooleanField(default=False))]