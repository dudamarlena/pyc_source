# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adminlteui/migrations/0002_options_valid.py
# Compiled at: 2020-01-21 04:26:45
# Size of source mod 2**32: 411 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_admin_settings', '0001_initial')]
    operations = [
     migrations.AddField(model_name='options',
       name='valid',
       field=models.BooleanField(default=True, verbose_name='Valid'))]