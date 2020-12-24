# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0012_auto_20170619_1648.py
# Compiled at: 2018-10-05 12:53:01
# Size of source mod 2**32: 873 bytes
from django.db import migrations
import django.db.models.deletion, djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0011_user_permission_mapping')]
    operations = [
     migrations.AddField(model_name='user',
       name='organization',
       field=djangoplus.db.models.fields.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='admin.Organization', verbose_name='Organização')),
     migrations.AddField(model_name='user',
       name='unit',
       field=djangoplus.db.models.fields.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='admin.Unit', verbose_name='Unidade'))]