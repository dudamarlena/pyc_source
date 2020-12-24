# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0006_remove_dancetypelevel_requiresaudition.py
# Compiled at: 2019-04-03 22:56:25
# Size of source mod 2**32: 408 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0005_auto_20170614_1607')]
    operations = [
     migrations.RemoveField(model_name='dancetypelevel',
       name='requiresAudition')]