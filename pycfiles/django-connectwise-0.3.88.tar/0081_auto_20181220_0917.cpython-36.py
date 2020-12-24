# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0081_auto_20181220_0917.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 471 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0080_auto_20181210_0930')]
    operations = [
     migrations.AlterField(model_name='member',
       name='avatar',
       field=models.CharField(blank=True, help_text='Member Avatar', max_length=250, null=True, verbose_name='Member Avatar'))]