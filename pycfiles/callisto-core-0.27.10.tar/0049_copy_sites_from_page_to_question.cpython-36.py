# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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