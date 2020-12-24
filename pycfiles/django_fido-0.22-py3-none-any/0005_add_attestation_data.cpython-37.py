# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/migrations/0005_add_attestation_data.py
# Compiled at: 2019-09-25 06:48:47
# Size of source mod 2**32: 466 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_fido', '0004_remove_u2f_device')]
    operations = [
     migrations.AddField(model_name='authenticator',
       name='attestation_data',
       field=models.TextField(null=True))]