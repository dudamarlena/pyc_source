# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0006_many_sites.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1207 bytes
from __future__ import unicode_literals
from django.db import migrations, models

def copy_site_to_sites(apps, schema_editor):
    current_database = schema_editor.connection.alias
    PageBase = apps.get_model('wizard_builder.PageBase')
    for page in PageBase.objects.using(current_database).filter(site__isnull=False):
        page.sites.add(page.site.id)


def copy_sites_to_site(apps, schema_editor):
    current_database = schema_editor.connection.alias
    PageBase = apps.get_model('wizard_builder.PageBase')
    for page in PageBase.objects.using(current_database):
        site_id = page.sites.first().id
        PageBase.objects.using(current_database).update(site=site_id)


class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0005_delete_constraints')]
    operations = [
     migrations.AddField(model_name='pagebase',
       name='sites',
       field=models.ManyToManyField(to='sites.Site')),
     migrations.RunPython(copy_site_to_sites, reverse_code=copy_sites_to_site),
     migrations.RemoveField(model_name='pagebase', name='site')]