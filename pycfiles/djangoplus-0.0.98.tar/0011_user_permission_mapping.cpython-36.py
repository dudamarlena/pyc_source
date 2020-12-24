# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/admin/migrations/0011_user_permission_mapping.py
# Compiled at: 2018-09-24 08:48:06
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