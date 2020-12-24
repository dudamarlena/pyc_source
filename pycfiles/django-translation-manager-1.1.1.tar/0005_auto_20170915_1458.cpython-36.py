# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/migrations/0005_auto_20170915_1458.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 1623 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('translation_manager', '0004_set_new_relative_paths')]
    operations = [
     migrations.CreateModel(name='RemoteTranslationEntry',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'remote_translation', models.TextField(blank=True, verbose_name='admin-remote_translation_ent22222222ry-remote_translation-label')),
      (
       'remote_changed', models.DateTimeField(auto_now=True, verbose_name='admin-remote_translation_entry-changed-label'))]),
     migrations.AlterModelOptions(name='translationbackup',
       options={'ordering':('-created', ), 
      'verbose_name':'Language backup',  'verbose_name_plural':'Language backups'}),
     migrations.AlterModelOptions(name='translationentry',
       options={'ordering':('original', ), 
      'permissions':(('load', 'admin-translation_entry-load-from-po'), ),  'verbose_name':'Translation entry',  'verbose_name_plural':'Translation entries'}),
     migrations.AddField(model_name='remotetranslationentry',
       name='translation_entry',
       field=models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), to='translation_manager.TranslationEntry'))]