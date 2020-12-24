# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/corporate_memberships/migrations/0015_auto_20180114_1155.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 938 bytes
from django.db import migrations

def add_reps_groups(apps, schema_editor):
    from tendenci.apps.corporate_memberships.models import CorpMembershipApp, CorpMembershipRep
    current_app = CorpMembershipApp.objects.current_app()
    if current_app:
        if not (current_app.dues_reps_group and current_app.member_reps_group):
            current_app.save()
        for rep in CorpMembershipRep.objects.filter():
            rep.sync_reps_groups()


class Migration(migrations.Migration):
    dependencies = [
     ('corporate_memberships', '0014_auto_20180114_1144')]
    operations = [
     migrations.RunPython(add_reps_groups)]