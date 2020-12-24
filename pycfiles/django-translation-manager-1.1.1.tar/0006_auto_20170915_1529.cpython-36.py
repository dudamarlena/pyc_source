# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/migrations/0006_auto_20170915_1529.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 1426 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('translation_manager', '0005_auto_20170915_1458')]
    operations = [
     migrations.CreateModel(name='ProxyTranslationEntry',
       fields=[],
       options={'proxy': True},
       bases=('translation_manager.translationentry', )),
     migrations.RenameField(model_name='remotetranslationentry',
       old_name='remote_changed',
       new_name='changed'),
     migrations.RemoveField(model_name='remotetranslationentry',
       name='remote_translation'),
     migrations.AddField(model_name='remotetranslationentry',
       name='translation',
       field=models.TextField(blank=True, verbose_name='admin-remote_translation_entry-remote_translation-label')),
     migrations.AlterField(model_name='remotetranslationentry',
       name='translation_entry',
       field=models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), related_name='remote_translation_entry', to='translation_manager.TranslationEntry'))]