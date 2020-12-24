# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/migrations/0012_authenticator_label.py
# Compiled at: 2020-01-30 08:13:30
# Size of source mod 2**32: 488 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_fido', '0011_remove_credential_data')]
    operations = [
     migrations.AddField(model_name='authenticator',
       name='label',
       field=models.TextField(blank=True, max_length=255, null=True))]