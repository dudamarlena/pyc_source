# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/migrations/0004_set_new_relative_paths.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 984 bytes
from __future__ import unicode_literals
from django.db import migrations
from translation_manager.settings import get_settings
from django.conf import settings
import os

def set_rels(apps, schema_editor):
    TranslationEntry = apps.get_model('translation_manager', 'TranslationEntry')
    for row in TranslationEntry.objects.all():
        row.locale_path = os.path.relpath(settings.LOCALE_PATHS[0], get_settings('TRANSLATIONS_BASE_DIR'))
        row.save()

    TranslationBackup = apps.get_model('translation_manager', 'TranslationBackup')
    for row in TranslationBackup.objects.all():
        row.locale_path = os.path.relpath(settings.LOCALE_PATHS[0], get_settings('TRANSLATIONS_BASE_DIR'))
        row.save()


class Migration(migrations.Migration):
    dependencies = [
     ('translation_manager', '0003_auto_20160926_0856')]
    operations = [
     migrations.RunPython(set_rels)]