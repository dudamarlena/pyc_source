# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/liveblog/migrations/0002_liveblogresponse_internal_name.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 431 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('liveblog', '0001_initial')]
    operations = [
     migrations.AddField(model_name='liveblogresponse', name='internal_name', field=models.CharField(max_length=255, blank=True, null=True))]