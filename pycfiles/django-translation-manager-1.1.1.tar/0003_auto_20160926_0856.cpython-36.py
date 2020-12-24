# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/migrations/0003_auto_20160926_0856.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 923 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('translation_manager', '0002_auto_20160920_1155')]
    operations = [
     migrations.AlterModelOptions(name='translationbackup',
       options={'ordering':('-created', ), 
      'verbose_name':'Admin-translation_backup-singular',  'verbose_name_plural':'Admin-translation_backup-plural'}),
     migrations.AlterModelOptions(name='translationentry',
       options={'ordering':('original', ), 
      'permissions':(('load', 'admin-translation_entry-load-from-po'), ),  'verbose_name':'Admin-translation_entry-singular', 
      'verbose_name_plural':'Admin-translation_entry-plural'})]