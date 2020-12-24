# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0005_auto_20161005_1536.py
# Compiled at: 2018-10-05 12:53:01
# Size of source mod 2**32: 677 bytes
from django.db import migrations
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0004_auto_20161001_1750')]
    operations = [
     migrations.AlterField(model_name='settings',
       name='theme',
       field=djangoplus.db.models.fields.CharField(choices=[[b'skin-7', b'skin-7'], [b'skin-6', b'skin-6'], [b'skin-5', b'skin-5'], [b'skin-4', b'skin-4'], [b'skin-3', b'skin-3'], [b'skin-2', b'skin-2'], [b'skin-1', b'skin-1']], default=b'skin-6', max_length=255, verbose_name='Tema'))]