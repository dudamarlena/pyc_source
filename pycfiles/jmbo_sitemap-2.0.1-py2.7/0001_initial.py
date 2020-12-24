# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_sitemap/migrations/0001_initial.py
# Compiled at: 2015-04-30 04:00:31
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('jmbo_sitemap_htmlsitemap', (
         (
          'preferences_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['preferences.Preferences'], unique=True, primary_key=True)),
         (
          'content', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
         (
          'draft', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True))))
        db.send_create_signal('jmbo_sitemap', ['HTMLSitemap'])

    def backwards(self, orm):
        db.delete_table('jmbo_sitemap_htmlsitemap')

    models = {'jmbo_sitemap.htmlsitemap': {'Meta': {'object_name': 'HTMLSitemap', '_ormbases': ['preferences.Preferences']}, 'content': (
                                              'ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}), 
                                    'draft': (
                                            'ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}), 
                                    'preferences_ptr': (
                                                      'django.db.models.fields.related.OneToOneField', [], {'to': "orm['preferences.Preferences']", 'unique': 'True', 'primary_key': 'True'})}, 
       'preferences.preferences': {'Meta': {'object_name': 'Preferences'}, 'id': (
                                        'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                   'sites': (
                                           'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'})}, 
       'sites.site': {'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"}, 'domain': (
                               'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                      'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'max_length': '50'})}}
    complete_apps = [
     'jmbo_sitemap']