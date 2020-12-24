# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/files/migrations/0006_auto_20181115_2145.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 664 bytes
from django.db import migrations

def populate_default_group(apps, schema_editor):
    from tendenci.apps.user_groups.utils import get_default_group
    try:
        group_id = get_default_group()
        File = apps.get_model('files', 'File')
        File.objects.filter(group=None).update(group_id=group_id)
    except:
        pass


class Migration(migrations.Migration):
    dependencies = [
     ('files', '0005_auto_20180724_1745'),
     ('user_groups', '0003_group_show_for_events')]
    operations = [
     migrations.RunPython(populate_default_group)]