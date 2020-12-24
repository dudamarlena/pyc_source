# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0011_user_permission_mapping.py
# Compiled at: 2018-10-05 12:53:01
# Size of source mod 2**32: 504 bytes
from django.db import migrations
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0010_auto_20170428_1545')]
    operations = [
     migrations.AddField(model_name='user',
       name='permission_mapping',
       field=djangoplus.db.models.fields.JsonField(verbose_name='Mapeamento de Permissão', null=True))]