# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/corporate_memberships/migrations/0004_auto_20151120_1538.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 708 bytes
from django.db import migrations

def threshold_copyto_cap(apps, schema_editor):
    CorporateMembershipType = apps.get_model('corporate_memberships', 'CorporateMembershipType')
    for corp_type in CorporateMembershipType.objects.all():
        if corp_type.apply_threshold:
            corp_type.apply_cap = True
            corp_type.membership_cap = corp_type.individual_threshold
            corp_type.save()


class Migration(migrations.Migration):
    dependencies = [
     ('corporate_memberships', '0003_auto_20151120_1531')]
    operations = [
     migrations.RunPython(threshold_copyto_cap)]