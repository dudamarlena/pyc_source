# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0022_auto_20180823_1947.py
# Compiled at: 2019-04-03 22:56:26
# Size of source mod 2**32: 490 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0021_auto_20180810_1634')]
    operations = [
     migrations.AlterModelOptions(name='event',
       options={'ordering':('-startTime', ), 
      'verbose_name':'Series/Event',  'verbose_name_plural':'All Series/Events'})]