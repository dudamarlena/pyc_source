# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/contributions/migrations/0008_auto_20160517_1413.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 490 bytes
from __future__ import unicode_literals
from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     ('contributions', '0007_auto_20160122_1459')]
    operations = [
     migrations.AlterField(model_name='lineitem', name='contributor', field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='line_items'))]