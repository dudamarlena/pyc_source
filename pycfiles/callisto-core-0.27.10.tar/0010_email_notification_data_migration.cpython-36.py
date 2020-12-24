# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0010_email_notification_data_migration.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1598 bytes
from __future__ import unicode_literals
from django.db import migrations

def update_content_types(source, apps, schema_editor):
    db_alias = schema_editor.connection.alias
    ContentType = apps.get_model('contenttypes', 'ContentType')
    content_type = ContentType.objects.using(db_alias).filter(app_label=source,
      model='emailnotification').delete()


def update_content_types_forward(apps, schema_editor):
    update_content_types('delivery', apps, schema_editor)


def update_content_types_reverse(apps, schema_editor):
    update_content_types('notification', apps, schema_editor)


class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0009_to_address_to_textfield')]
    database_operations = []
    state_operations = []
    operations = []