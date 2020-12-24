# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0029_auto_20180430_1924.py
# Compiled at: 2018-04-30 13:24:49
# Size of source mod 2**32: 979 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0028_auto_20180430_1919')]
    operations = [
     migrations.RemoveField(model_name='incomingalbaran', name='code'),
     migrations.RemoveField(model_name='incomingalbaran', name='code_counter'),
     migrations.RemoveField(model_name='outgoingalbaran', name='code'),
     migrations.RemoveField(model_name='outgoingalbaran', name='code_counter'),
     migrations.RemoveField(model_name='requeststock', name='code'),
     migrations.RemoveField(model_name='requeststock', name='code_counter')]