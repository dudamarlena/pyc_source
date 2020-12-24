# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_table/migrations/0002_tablepluginmodel_filter.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 501 bytes
from __future__ import unicode_literals
from django.db import migrations
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [
     ('cms_qe_table', '0001_initial')]
    operations = [
     migrations.AddField(model_name='tablepluginmodel', name='filter', field=jsonfield.fields.JSONField(default=dict, verbose_name='Filter'))]