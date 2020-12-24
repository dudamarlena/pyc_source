# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/staff/migrations/0005_auto_20180126_1719.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 628 bytes
from django.db import migrations

def make_slug_unique(apps, schema_editor):
    """
        The slug field should be unique
    """
    Staff = apps.get_model('staff', 'Staff')
    for staff in Staff.objects.all():
        if Staff.objects.filter(slug=(staff.slug)).exclude(id=(staff.id)).exists():
            staff.slug = '{0}-{1}'.format(staff.slug[:75 - len(str(staff.id)) - 1], staff.id)
            staff.save()


class Migration(migrations.Migration):
    dependencies = [
     ('staff', '0004_auto_20170309_1510')]
    operations = [
     migrations.RunPython(make_slug_unique)]