# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/aluminium/ninecms/migrations/0004_auto_20150624_1131.py
# Compiled at: 2015-06-25 09:56:49
# Size of source mod 2**32: 511 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ninecms', '0003_auto_20150623_1731')]
    operations = [
     migrations.AlterModelOptions(name='node', options={'permissions': (('access_toolbar', 'Can access the CMS toolbar'), ('use_full_html', 'Can use Full HTML in node body and summary'),
 ('list_nodes', 'Can list nodes'))})]