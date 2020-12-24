# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0021_user_uuid_now_unique.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 496 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0020_generate_user_uuids')]
    operations = [
     migrations.AlterField(model_name='user', name='uuid', field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True))]