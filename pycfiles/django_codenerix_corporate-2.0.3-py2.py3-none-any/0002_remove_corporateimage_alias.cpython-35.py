# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_corporate/migrations/0002_remove_corporateimage_alias.py
# Compiled at: 2018-01-18 06:08:13
# Size of source mod 2**32: 401 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_corporate', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name='corporateimage', name='alias')]