# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cristian/projects/python/django-qa/qa/migrations/0004_answer_updated.py
# Compiled at: 2018-03-17 13:09:30
# Size of source mod 2**32: 591 bytes
from __future__ import unicode_literals
from django.db import models, migrations
import datetime
from django.utils.timezone import utc

class Migration(migrations.Migration):
    dependencies = [
     ('qa', '0003_auto_20160414_1413')]
    operations = [
     migrations.AddField(model_name='answer',
       name='updated',
       field=models.DateTimeField(default=datetime.datetime(2016, 5, 5, 16, 11, 48, 760837, tzinfo=utc), verbose_name=b'date updated', auto_now=True),
       preserve_default=False)]