# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/migrations/0009_fill_credential_ids.py
# Compiled at: 2019-09-25 06:48:47
# Size of source mod 2**32: 813 bytes
from __future__ import unicode_literals
import base64
from django.db import migrations

def fill_credential_ids(apps, schema_editor):
    Authenticator = apps.get_model('django_fido', 'Authenticator')
    db_alias = schema_editor.connection.alias
    for authenticator in Authenticator.objects.all():
        authenticator.credential_id_data = base64.b64encode(authenticator.credential.credential_id).decode('utf-8')
        authenticator.save()


class Migration(migrations.Migration):
    dependencies = [
     ('django_fido', '0008_add_credential_id')]
    operations = [
     migrations.RunPython(fill_credential_ids, reverse_code=(migrations.RunPython.noop), elidable=True)]