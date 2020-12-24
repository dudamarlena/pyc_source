# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/migrations/0001_initial.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 3386 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='TranslationBackup',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='admin-translation_backup-created-label')),
      (
       'changed', models.DateTimeField(auto_now=True, verbose_name='admin-translation_backup-changed-label')),
      (
       'language', models.CharField(db_index=True, max_length=5, verbose_name='admin-translation_backup-language-label')),
      (
       'locale_path', models.CharField(db_index=True, max_length=256, verbose_name='admin-translation_backup-locale_path-label')),
      (
       'locale_parent_dir', models.CharField(db_index=True, max_length=256, verbose_name='admin-translation_backup-locale_parent_dir-label')),
      (
       'domain', models.CharField(db_index=True, max_length=256, verbose_name='admin-translation_backup-domain-label')),
      (
       'content', models.TextField(verbose_name='admin-translation_backup-content'))],
       options={'ordering':('-created', ), 
      'verbose_name':'Language backup', 
      'verbose_name_plural':'Language backups'}),
     migrations.CreateModel(name='TranslationEntry',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='admin-translation_entry-created-label')),
      (
       'changed', models.DateTimeField(auto_now=True, verbose_name='admin-translation_entry-changed-label')),
      (
       'language', models.CharField(db_index=True, max_length=5, verbose_name='admin-translation_entry-language-label')),
      (
       'original', models.TextField(verbose_name='admin-translation_entry-original-label')),
      (
       'translation', models.TextField(blank=True, verbose_name='admin-translation_entry-translation-label')),
      (
       'occurrences', models.TextField(blank=True, verbose_name='admin-translation_entry-occurrences-label')),
      (
       'is_published', models.BooleanField(default=True, editable=False, verbose_name='admin-translation_entry-is_published-label')),
      (
       'locale_path', models.CharField(db_index=True, max_length=256, verbose_name='admin-translation_entry-locale_path-label')),
      (
       'locale_parent_dir', models.CharField(db_index=True, max_length=256, verbose_name='admin-translation_entry-locale_parent_dir-label')),
      (
       'domain', models.CharField(db_index=True, max_length=256, verbose_name='admin-translation_entry-domain-label'))],
       options={'ordering':('original', ), 
      'verbose_name':'Translation entry', 
      'verbose_name_plural':'Translation entries', 
      'permissions':(('load', 'admin-translation_entry-load-from-po'), )})]