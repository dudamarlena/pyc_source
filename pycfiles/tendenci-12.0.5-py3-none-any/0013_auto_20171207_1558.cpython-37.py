# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/corporate_memberships/migrations/0013_auto_20171207_1558.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 829 bytes
from django.db import migrations

def parent_entity_assign_default(apps, schema_editor):
    """
    Assign the default entity to the parent_entity field for existing corp profiles.
    """
    CorpProfile = apps.get_model('corporate_memberships', 'CorpProfile')
    Entity = apps.get_model('entities', 'Entity')
    corp_profiles = CorpProfile.objects.all()
    default_entity = Entity.objects.first()
    for corp_profile in corp_profiles:
        if not corp_profile.parent_entity:
            corp_profile.parent_entity = default_entity
            corp_profile.save()


class Migration(migrations.Migration):
    dependencies = [
     ('corporate_memberships', '0012_corpmembershipapp_parent_entities')]
    operations = [
     migrations.RunPython(parent_entity_assign_default)]