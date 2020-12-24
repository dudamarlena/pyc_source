# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/migrations/0005_auto_20170214.py
# Compiled at: 2018-02-03 12:24:20
# Size of source mod 2**32: 620 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('common', '0004_auto_20161219')]
    operations = [
     migrations.AlterField(model_name='metadata',
       name='key',
       field=models.CharField(db_index=True, max_length=100, verbose_name='clé')),
     migrations.AlterIndexTogether(name='metadata',
       index_together=(set([('key', 'deletion_date')])))]