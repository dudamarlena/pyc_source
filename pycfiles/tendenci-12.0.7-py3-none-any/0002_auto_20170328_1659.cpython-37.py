# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/locations/migrations/0002_auto_20170328_1659.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 765 bytes
from django.db import migrations
from django.template.defaultfilters import slugify

def assign_slug(apps, schema_editor):
    """
        Assign value to the slug field if slug is blank for locations
    """
    Location = apps.get_model('locations', 'Location')
    for location in Location.objects.all():
        if not location.slug:
            slug = slugify(location.location_name)
            if Location.objects.filter(slug=slug).exists():
                slug = '%s%s' % (slug, location.id)
            location.slug = slug
            location.save()


class Migration(migrations.Migration):
    dependencies = [
     ('locations', '0001_initial')]
    operations = [
     migrations.RunPython(assign_slug)]