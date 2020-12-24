# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0004_auto_20161001_1750.py
# Compiled at: 2018-10-05 12:53:01
# Size of source mod 2**32: 1291 bytes
from django.db import migrations
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0003_auto_20160914_1821')]
    operations = [
     migrations.RemoveField(model_name='settings',
       name='default_color'),
     migrations.AddField(model_name='settings',
       name='sidebar_fixed',
       field=djangoplus.db.models.fields.BooleanField(default=False, verbose_name='Fixo')),
     migrations.AddField(model_name='settings',
       name='sidebar_hidden',
       field=djangoplus.db.models.fields.BooleanField(default=False, verbose_name='Escondido')),
     migrations.AddField(model_name='settings',
       name='sidebar_mini',
       field=djangoplus.db.models.fields.BooleanField(default=False, verbose_name='Compacto')),
     migrations.AddField(model_name='settings',
       name='theme',
       field=djangoplus.db.models.fields.CharField(choices=[[b'skin-6', b'skin-6'], [b'skin-5', b'skin-5']], default=b'skin-6', max_length=255, verbose_name='Tema'))]