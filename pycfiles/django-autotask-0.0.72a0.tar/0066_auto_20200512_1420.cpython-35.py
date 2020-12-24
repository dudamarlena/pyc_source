# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0066_auto_20200512_1420.py
# Compiled at: 2020-05-12 17:39:24
# Size of source mod 2**32: 442 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0065_auto_20200512_1224')]
    operations = [
     migrations.AlterField(model_name='ticket', name='estimated_hours', field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True))]