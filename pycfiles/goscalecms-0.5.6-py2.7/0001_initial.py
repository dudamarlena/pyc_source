# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/themes/migrations/0001_initial.py
# Compiled at: 2013-01-28 01:18:40
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('themes_theme', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
         (
          'theme_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True))))
        db.send_create_signal('themes', ['Theme'])
        db.create_table('themes_theme_sites', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'theme', models.ForeignKey(orm['themes.theme'], null=False)),
         (
          'site', models.ForeignKey(orm['sites.site'], null=False))))
        db.create_unique('themes_theme_sites', ['theme_id', 'site_id'])

    def backwards(self, orm):
        db.delete_table('themes_theme')
        db.delete_table('themes_theme_sites')

    models = {'sites.site': {'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"}, 'domain': (
                               'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                      'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'max_length': '50'})}, 
       'themes.theme': {'Meta': {'object_name': 'Theme'}, 'id': (
                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                        'name': (
                               'django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}), 
                        'sites': (
                                'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'themes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sites.Site']"}), 
                        'theme_file': (
                                     'django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})}}
    complete_apps = [
     'themes']