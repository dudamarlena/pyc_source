# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0018_user_uuid.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 491 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0017_userprofile_causes')]
    operations = [
     migrations.AddField(model_name='user', name='uuid', field=models.UUIDField(default=uuid.uuid4, editable=False, null=True))]