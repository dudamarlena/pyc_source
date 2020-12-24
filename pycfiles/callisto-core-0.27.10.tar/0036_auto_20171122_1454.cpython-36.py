# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0036_auto_20171122_1454.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 410 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0035_auto_20171122_1454')]
    operations = [
     migrations.RemoveField(model_name='sentreport', name='polymorphic_ctype'),
     migrations.DeleteModel(name='SentReport')]