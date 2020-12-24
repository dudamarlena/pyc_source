# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0061_auto_20200416_1241.py
# Compiled at: 2020-05-08 13:23:41
# Size of source mod 2**32: 410 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0060_auto_20200414_1522')]
    operations = [
     migrations.AlterModelOptions(name='servicecallstatus', options={'ordering': ('label', ), 'verbose_name_plural': 'Service call statuses'})]