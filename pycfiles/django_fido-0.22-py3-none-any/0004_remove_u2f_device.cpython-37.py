# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/migrations/0004_remove_u2f_device.py
# Compiled at: 2019-09-25 06:48:47
# Size of source mod 2**32: 471 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('django_fido', '0003_add_authenticator')]
    operations = [
     migrations.RemoveField(model_name='u2fdevice',
       name='user'),
     migrations.DeleteModel(name='U2fDevice')]