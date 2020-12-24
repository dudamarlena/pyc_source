# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0026_auto_20191125_0952.py
# Compiled at: 2019-11-26 13:56:53
# Size of source mod 2**32: 366 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0025_auto_20191125_0939')]
    operations = [
     migrations.AlterModelOptions(name='priority', options={'verbose_name_plural': 'Priorities'})]