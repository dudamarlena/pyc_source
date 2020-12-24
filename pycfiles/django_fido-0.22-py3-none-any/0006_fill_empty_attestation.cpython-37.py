# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/migrations/0006_fill_empty_attestation.py
# Compiled at: 2019-09-25 06:48:47
# Size of source mod 2**32: 529 bytes
from __future__ import unicode_literals
from django.db import migrations
SQL = "UPDATE django_fido_authenticator SET attestation_data = 'owFkbm9uZQJYJTAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwAAAAACoDoA=='"

class Migration(migrations.Migration):
    dependencies = [
     ('django_fido', '0005_add_attestation_data')]
    operations = [
     migrations.RunSQL(SQL, reverse_sql=(migrations.RunSQL.noop), elidable=True)]