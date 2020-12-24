# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/saltstack/migrations/0005_label_change.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('saltstack', '0004_remove_spl_state')]
    operations = [
     migrations.AlterModelOptions(name=b'saltstackservice', options={b'verbose_name': b'SaltStack service', b'verbose_name_plural': b'SaltStack service'})]