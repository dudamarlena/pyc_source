# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0019_auto_20171119_1543.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 997 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0018_remove_matchreport_identifier')]
    operations = [
     migrations.AlterField(model_name='matchreport',
       name='encode_prefix',
       field=models.TextField(blank=True)),
     migrations.AlterField(model_name='matchreport',
       name='salt',
       field=models.TextField(null=True)),
     migrations.AlterField(model_name='report',
       name='encode_prefix',
       field=models.TextField(blank=True, null=True)),
     migrations.AlterField(model_name='report',
       name='salt',
       field=models.TextField(null=True)),
     migrations.AlterField(model_name='sentreport',
       name='to_address',
       field=(models.TextField()))]