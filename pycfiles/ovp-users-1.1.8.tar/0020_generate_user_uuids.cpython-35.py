# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0020_generate_user_uuids.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 557 bytes
from __future__ import unicode_literals
from django.db import migrations
import uuid

def gen_uuid(apps, schema_editor):
    Model = apps.get_model('ovp_users', 'User')
    for user in Model.objects.all():
        user.uuid = uuid.uuid4()
        user.save()


class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0019_userprofile_public')]
    operations = [
     migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop)]