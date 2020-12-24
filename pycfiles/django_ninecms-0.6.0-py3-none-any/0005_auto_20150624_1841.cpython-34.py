# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/aluminium/ninecms/migrations/0005_auto_20150624_1841.py
# Compiled at: 2015-06-25 09:56:49
# Size of source mod 2**32: 638 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ninecms', '0004_auto_20150624_1131')]
    operations = [
     migrations.AlterModelOptions(name='pagetype', options={'permissions': (('list_nodes_pagetype', 'List nodes of a specific page type'), ('add_node_pagetype', 'Add node of a specific page type'),
 ('change_node_pagetype', 'Change node of a specific page type'), ('delete_node_pagetype', 'Delete node of a specific page type')),  'ordering': ['id']})]