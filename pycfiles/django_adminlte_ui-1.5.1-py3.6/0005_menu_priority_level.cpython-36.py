# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adminlteui/migrations/0005_menu_priority_level.py
# Compiled at: 2020-05-05 22:21:28
# Size of source mod 2**32: 436 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_admin_settings', '0004_auto_20190708_1832')]
    operations = [
     migrations.AddField(model_name='menu',
       name='priority_level',
       field=models.IntegerField(default=100, verbose_name='Priority Level'))]