# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/poll/migrations/0002_auto_20160311_1034.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 797 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import djbetty.fields

class Migration(migrations.Migration):
    dependencies = [
     ('poll', '0001_initial')]
    operations = [
     migrations.AddField(model_name='answer', name='answer_image', field=djbetty.fields.ImageField(default=None, null=True, blank=True)),
     migrations.AddField(model_name='poll', name='answer_type', field=models.TextField(default=b'text', blank=True)),
     migrations.AddField(model_name='poll', name='poll_image', field=djbetty.fields.ImageField(default=None, null=True, blank=True))]