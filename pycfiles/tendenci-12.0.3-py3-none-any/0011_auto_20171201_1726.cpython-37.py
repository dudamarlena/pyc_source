# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/corporate_memberships/migrations/0011_auto_20171201_1726.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 973 bytes
from django.db import migrations

def add_parent_entity_to_existing_apps(apps, schema_editor):
    CorpMembershipApp = apps.get_model('corporate_memberships', 'CorpMembershipApp')
    CorpMembershipAppField = apps.get_model('corporate_memberships', 'CorpMembershipAppField')
    corp_apps = CorpMembershipApp.objects.all()
    for corp_app in corp_apps:
        if not CorpMembershipAppField.objects.filter(corp_app=corp_app, field_name='parent_entity').exists():
            app_field = CorpMembershipAppField(corp_app=corp_app,
              label='Parent Entity',
              field_name='parent_entity',
              display=False)
            app_field.save()


class Migration(migrations.Migration):
    dependencies = [
     ('corporate_memberships', '0010_auto_20171201_1721')]
    operations = [
     migrations.RunPython(add_parent_entity_to_existing_apps)]