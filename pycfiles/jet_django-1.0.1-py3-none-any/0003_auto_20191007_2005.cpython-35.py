# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_django/jet_django/migrations/0003_auto_20191007_2005.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 1218 bytes
from django.db import connection, migrations

def load(apps, schema_editor):
    with connection.cursor() as (cursor):
        cursor.execute('SELECT token, date_add FROM jet_django_token')
        old_token = cursor.fetchone()
        if not old_token:
            return
        cursor.execute('SELECT id FROM __jet__token')
        new_token = cursor.fetchone()
        if new_token is None:
            cursor.execute('INSERT INTO __jet__token (token, date_add) VALUES (%s, %s)', [
             old_token[0].hex,
             old_token[1]])
        else:
            cursor.execute('UPDATE __jet__token SET token = %s, date_add = %s WHERE id = %s', [
             old_token[0].hex,
             old_token[1],
             new_token[0]])


class Migration(migrations.Migration):
    dependencies = [
     ('jet_django', '0002_auto_20181014_2002')]
    operations = [
     migrations.AlterModelOptions(name='token', options={'managed': False, 'verbose_name': 'token', 'verbose_name_plural': 'tokens'}),
     migrations.RunPython(load, reverse_code=lambda a, b: ())]