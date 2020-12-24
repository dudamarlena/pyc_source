# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/migrations/0008_auto_20180302.py
# Compiled at: 2018-03-02 06:56:09
# Size of source mod 2**32: 520 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     ('common', '0007_auto_20180210')]
    operations = [
     migrations.AlterIndexTogether(name='metadata',
       index_together={
      ('content_type', 'object_id', 'deletion_date', 'key'), ('content_type', 'object_id'), ('content_type', 'object_id', 'deletion_date')})]