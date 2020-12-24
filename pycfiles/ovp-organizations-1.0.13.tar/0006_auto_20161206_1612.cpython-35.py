# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0006_auto_20161206_1612.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 922 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_organizations', '0005_auto_20161206_1515')]
    operations = [
     migrations.RenameField(model_name='organization', old_name='created_at', new_name='created_date'),
     migrations.RenameField(model_name='organization', old_name='deleted_at', new_name='deleted_date'),
     migrations.RenameField(model_name='organization', old_name='modified_at', new_name='modified_date'),
     migrations.RenameField(model_name='organization', old_name='published_at', new_name='published_date')]