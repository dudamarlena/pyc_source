# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0015_settings_company.py
# Compiled at: 2018-10-05 12:53:01
# Size of source mod 2**32: 505 bytes
from django.db import migrations
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0014_auto_20180106_1921')]
    operations = [
     migrations.AddField(model_name='settings',
       name='company',
       field=djangoplus.db.models.fields.CharField(blank=True, max_length=255, null=True, verbose_name='Empresa'))]