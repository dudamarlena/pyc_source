# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/migrations/0006_auto_20170905.py
# Compiled at: 2018-02-03 12:24:20
# Size of source mod 2**32: 1292 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     ('common', '0005_auto_20170214')]
    operations = [
     migrations.AlterField(model_name='history',
       name='object_uid',
       field=models.UUIDField(editable=False, verbose_name='UUID')),
     migrations.AlterField(model_name='historyfield',
       name='field_name',
       field=models.CharField(editable=False, max_length=100, verbose_name='nom du champ')),
     migrations.AlterField(model_name='metadata',
       name='deletion_date',
       field=models.DateTimeField(blank=True, null=True, verbose_name='date de suppression')),
     migrations.AlterField(model_name='metadata',
       name='key',
       field=models.CharField(max_length=100, verbose_name='clé')),
     migrations.AlterIndexTogether(name='metadata',
       index_together=(set([('content_type', 'object_id', 'key', 'deletion_date')])))]