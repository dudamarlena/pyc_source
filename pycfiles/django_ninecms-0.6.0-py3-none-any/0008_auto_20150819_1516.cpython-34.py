# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/aluminium/ninecms/migrations/0008_auto_20150819_1516.py
# Compiled at: 2015-08-27 05:04:22
# Size of source mod 2**32: 477 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ninecms', '0007_auto_20150727_1833')]
    operations = [
     migrations.AlterField(model_name='taxonomyterm', name='description_node', field=models.ForeignKey(related_name='term_described', blank=True, to='ninecms.Node', null=True))]