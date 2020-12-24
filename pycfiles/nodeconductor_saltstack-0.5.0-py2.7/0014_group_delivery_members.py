# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/migrations/0014_group_delivery_members.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations
import gm2m.fields

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0001_initial'),
     ('exchange', '0013_remove_group_delivery_members')]
    operations = [
     migrations.AddField(model_name=b'group', name=b'delivery_members', field=gm2m.fields.GM2MField(through_fields=('gm2m_src',
                                                                                                               'gm2m_tgt',
                                                                                                               'gm2m_ct',
                                                                                                               'gm2m_pk')), preserve_default=True)]