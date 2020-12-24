# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0014_auto_20190414_1049.py
# Compiled at: 2019-04-14 09:49:48
# Size of source mod 2**32: 794 bytes
from django.db import migrations
import django.db.models.deletion, djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0013_auto_20190326_2256')]
    operations = [
     migrations.AddField(model_name='user',
       name='scope',
       field=djangoplus.db.models.fields.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='admin.Scope', verbose_name='Scope')),
     migrations.AlterField(model_name='settings',
       name='icon',
       field=djangoplus.db.models.fields.ImageField(blank=True, default=None, null=True, upload_to='config', verbose_name='Ícone'))]