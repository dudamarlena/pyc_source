# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0032_auto_20191129_1501.py
# Compiled at: 2019-12-04 18:09:39
# Size of source mod 2**32: 881 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0031_auto_20191129_1454')]
    operations = [
     migrations.AlterModelOptions(name='displaycolor', options={'ordering': ('label', ), 'verbose_name_plural': 'Display colors'}),
     migrations.AlterModelOptions(name='projectstatus', options={'ordering': ('label', ), 'verbose_name_plural': 'Project statuses'}),
     migrations.AlterModelOptions(name='queue', options={'ordering': ('label', ), 'verbose_name_plural': 'Queues'}),
     migrations.AlterModelOptions(name='status', options={'ordering': ('label', ), 'verbose_name_plural': 'Statuses'})]