# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo62/mogo/mqueue/migrations/0002_mevent_scope.py
# Compiled at: 2017-07-28 07:41:14
# Size of source mod 2**32: 597 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mqueue', '0001_initial')]
    operations = [
     migrations.AddField(model_name='mevent', name='scope', field=models.CharField(choices=[('superuser', 'Superuser'), ('staff', 'Staff'), ('users', 'Users'), ('user', 'User'), ('public', 'Public')], default='superuser', max_length=18, verbose_name='Scope'))]