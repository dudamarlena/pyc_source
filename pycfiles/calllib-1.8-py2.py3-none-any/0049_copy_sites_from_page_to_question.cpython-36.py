# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0049_copy_sites_from_page_to_question.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 654 bytes
from __future__ import unicode_literals
from django.db import migrations, models

def move_sites(apps, schema_editor):
    current_database = schema_editor.connection.alias
    Page = apps.get_model('wizard_builder.Page')
    for page in Page.objects.using(current_database):
        sites = page.sites.all()
        for question in page.formquestion_set.all():
            (question.sites.add)(*sites)


class Migration(migrations.Migration):
    dependencies = [
     ('sites', '0002_alter_domain_unique'),
     ('wizard_builder', '0048_formquestion_sites')]
    operations = [
     migrations.RunPython(move_sites, migrations.RunPython.noop)]