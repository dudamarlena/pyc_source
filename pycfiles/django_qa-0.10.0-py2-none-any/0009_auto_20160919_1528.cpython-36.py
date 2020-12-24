# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cristian/projects/python/django-qa/qa/migrations/0009_auto_20160919_1528.py
# Compiled at: 2018-03-17 13:09:30
# Size of source mod 2**32: 419 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('qa', '0008_auto_20160719_0729')]
    operations = [
     migrations.AlterModelOptions(name='answer',
       options={'ordering': ['answer', '-pub_date']})]