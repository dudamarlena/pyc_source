# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/migrations/0004_cmsentries_logo_url.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 533 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mycms', '0003_cmsentries_lists_include')]
    operations = [
     migrations.AddField(model_name='cmsentries',
       name='logo_url',
       field=models.CharField(blank=True, default='/static/mycms/images/png/default.png', max_length=1024, null=True))]