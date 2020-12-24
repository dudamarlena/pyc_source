# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/admin/migrations/0013_auto_20170910_1543.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 1600 bytes
from django.db import migrations
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0012_auto_20170619_1648')]
    operations = [
     migrations.RemoveField(model_name='settings',
       name='sidebar_fixed'),
     migrations.RemoveField(model_name='settings',
       name='sidebar_hidden'),
     migrations.RemoveField(model_name='settings',
       name='sidebar_mini'),
     migrations.RemoveField(model_name='settings',
       name='theme'),
     migrations.AlterField(model_name='organization',
       name='ascii',
       field=djangoplus.db.models.fields.SearchField(blank=True, default=b'', editable=False, null=True)),
     migrations.AlterField(model_name='settings',
       name='version',
       field=djangoplus.db.models.fields.CharField(max_length=255, null=True, verbose_name='Versão do Sistema')),
     migrations.AlterField(model_name='unit',
       name='ascii',
       field=djangoplus.db.models.fields.SearchField(blank=True, default=b'', editable=False, null=True)),
     migrations.AlterField(model_name='user',
       name='permission_mapping',
       field=djangoplus.db.models.fields.JsonField(verbose_name='Mapeamento de Permissão', null=True))]