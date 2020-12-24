# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/staff/migrations/0003_auto_20170303_1554.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 777 bytes
from django.db import migrations
from django.template.defaultfilters import slugify

def assign_slug(apps, schema_editor):
    """
        Assign value to the slug field for existing department rows
    """
    Department = apps.get_model('staff', 'Department')
    for department in Department.objects.all():
        if not department.slug:
            slug = slugify(department.name)
            if Department.objects.filter(slug=slug).exists():
                slug = '%s%s' % (slug, department.id)
            department.slug = slug
            department.save()


class Migration(migrations.Migration):
    dependencies = [
     ('staff', '0002_auto_20170303_1553')]
    operations = [
     migrations.RunPython(assign_slug)]