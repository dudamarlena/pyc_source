# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/django_sloop/migrations/0002_change_meta.py
# Compiled at: 2019-08-14 12:32:29
# Size of source mod 2**32: 394 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('django_sloop', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='pushmessage',
       options={'verbose_name':'Push Message', 
      'verbose_name_plural':'Push Messages'})]