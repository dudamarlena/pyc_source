# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/liveblog/migrations/0004_auto_20160908_1512.py
# Compiled at: 2016-09-28 11:20:42
# Size of source mod 2**32: 670 bytes
from __future__ import unicode_literals
from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     ('liveblog', '0003_auto_20160825_1459')]
    operations = [
     migrations.AlterField(model_name='liveblogentry', name='headline', field=models.CharField(max_length=255, null=True, blank=True)),
     migrations.AlterField(model_name='liveblogresponse', name='author', field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True))]