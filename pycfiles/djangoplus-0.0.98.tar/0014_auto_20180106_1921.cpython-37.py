# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0014_auto_20180106_1921.py
# Compiled at: 2018-10-05 12:53:01
# Size of source mod 2**32: 689 bytes
from django.db import migrations
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0013_auto_20170910_1543')]
    operations = [
     migrations.AlterField(model_name='organization',
       name='ascii',
       field=djangoplus.db.models.fields.SearchField(blank=True, default=b'', editable=False)),
     migrations.AlterField(model_name='unit',
       name='ascii',
       field=djangoplus.db.models.fields.SearchField(blank=True, default=b'', editable=False))]