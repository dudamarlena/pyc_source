# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0013_questionpage_to_page_2.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1469 bytes
from __future__ import unicode_literals
from django.db import migrations, models

def copy_questionpage_to_page(apps, schema_editor):
    current_database = schema_editor.connection.alias
    QuestionPage = apps.get_model('wizard_builder.QuestionPage')
    for question_page in QuestionPage.objects.using(current_database):
        with schema_editor.connection.cursor() as (cursor):
            cursor.execute('INSERT INTO "wizard_builder_page" ("id", "position", "section", "infobox") VALUES (%s, %s, %s, %s)', [
             question_page.id,
             question_page.position,
             question_page.section,
             question_page.infobox])
            for site in question_page.sites.all():
                cursor.execute('INSERT INTO "wizard_builder_page_sites" ("page_id", "site_id") VALUES (%s, %s)', [
                 question_page.id, site.id])


def delete_page_rows(apps, schema_editor):
    current_database = schema_editor.connection.alias
    Page = apps.get_model('wizard_builder.Page')
    Page.objects.using(current_database).delete()


class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0012_questionpage_to_page')]
    operations = [
     migrations.RunPython(copy_questionpage_to_page, delete_page_rows)]