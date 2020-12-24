# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/resumes/migrations/0004_auto_20190109_1714.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 854 bytes
from django.db import migrations

def populate_from_contact_name(apps, schema_editor):
    """
    Populate the first_name and last_name from the contact_name.
    """
    from nameparser import HumanName
    Resume = apps.get_model('resumes', 'Resume')
    for resume in Resume.objects.all():
        if resume.contact_name:
            name = HumanName(resume.contact_name)
            first_name, last_name = name.first, name.last
            if first_name or last_name:
                Resume.objects.filter(id=(resume.id)).update(first_name=first_name, last_name=last_name)


class Migration(migrations.Migration):
    dependencies = [
     ('resumes', '0003_auto_20190109_1714')]
    operations = [
     migrations.RunPython(populate_from_contact_name)]