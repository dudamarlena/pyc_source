# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/migrations/0011_auto_20190201.py
# Compiled at: 2019-02-02 11:40:33
# Size of source mod 2**32: 685 bytes
import common.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('common', '0010_auto_20181202')]
    operations = [
     migrations.AddField(model_name='history',
       name='collector_delete',
       field=common.fields.JsonField(blank=True, editable=False, null=True, verbose_name='suppressions')),
     migrations.AddField(model_name='history',
       name='collector_update',
       field=common.fields.JsonField(blank=True, editable=False, null=True, verbose_name='mises à jour'))]