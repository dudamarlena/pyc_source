# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/financial/migrations/0015_auto_20190403_1555.py
# Compiled at: 2019-04-03 22:56:30
# Size of source mod 2**32: 618 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('financial', '0014_auto_20190322_1729')]
    operations = [
     migrations.AlterModelOptions(name='repeatedexpenserule',
       options={'permissions':(('can_generate_repeated_expenses', 'Able to generate rule-based repeated expenses using the admin view'), ), 
      'verbose_name':'Repeated expense rule',  'verbose_name_plural':'Repeated expense rules'})]