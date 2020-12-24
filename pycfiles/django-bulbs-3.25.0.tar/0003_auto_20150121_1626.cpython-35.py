# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/promotion/migrations/0003_auto_20150121_1626.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 634 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('promotion', '0002_content_list_to_pzone')]
    operations = [
     migrations.AlterModelOptions(name='pzone', options={'ordering': ['name']}),
     migrations.AlterModelOptions(name='pzonehistory', options={'ordering': ['-date']}),
     migrations.AlterModelOptions(name='pzoneoperation', options={'ordering': ['when', 'id']})]