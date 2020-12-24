# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0011_auto_20190312_1716.py
# Compiled at: 2019-03-12 16:16:26
# Size of source mod 2**32: 993 bytes
from django.conf import settings
from django.db import migrations
import django.db.models.deletion, djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0010_auto_20190307_1656')]
    operations = [
     migrations.AlterModelOptions(name='user',
       options={'verbose_name':'Usuário', 
      'verbose_name_plural':'Usuários'}),
     migrations.AlterField(model_name='log',
       name='user',
       field=djangoplus.db.models.fields.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL), verbose_name='Usuário')),
     migrations.AlterField(model_name='role',
       name='user',
       field=djangoplus.db.models.fields.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL), verbose_name='Usuário'))]