# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/slideshow/migrations/0001_initial.py
# Compiled at: 2012-10-05 05:23:18
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('cmsplugin_slideshow', (
         (
          'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),))
        db.send_create_signal('slideshow', ['Slideshow'])
        db.create_table('slideshow_slide', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'ordering', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
         (
          'slideshow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['slideshow.Slideshow'])),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=216, null=True, blank=True)),
         (
          'summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
         (
          'picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
         (
          'picture_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
         (
          'picture_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
         (
          'alt', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
         (
          'url', self.gf('django.db.models.fields.CharField')(max_length=216)),
         (
          'publish', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True))))
        db.send_create_signal('slideshow', ['Slide'])

    def backwards(self, orm):
        db.delete_table('cmsplugin_slideshow')
        db.delete_table('slideshow_slide')

    models = {'cms.cmsplugin': {'Meta': {'object_name': 'CMSPlugin'}, 'creation_date': (
                                         'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                         'id': (
                              'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'language': (
                                    'django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}), 
                         'level': (
                                 'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                         'lft': (
                               'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                         'parent': (
                                  'django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}), 
                         'placeholder': (
                                       'django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}), 
                         'plugin_type': (
                                       'django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}), 
                         'position': (
                                    'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                         'rght': (
                                'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                         'tree_id': (
                                   'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})}, 
       'cms.placeholder': {'Meta': {'object_name': 'Placeholder'}, 'default_width': (
                                           'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'slot': (
                                  'django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})}, 
       'slideshow.slide': {'Meta': {'ordering': "('ordering',)", 'object_name': 'Slide'}, 'alt': (
                                 'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                           'date_created': (
                                          'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                           'date_updated': (
                                          'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'ordering': (
                                      'django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}), 
                           'picture': (
                                     'django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}), 
                           'picture_height': (
                                            'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}), 
                           'picture_width': (
                                           'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}), 
                           'publish': (
                                     'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                           'slideshow': (
                                       'django.db.models.fields.related.ForeignKey', [], {'to': "orm['slideshow.Slideshow']"}), 
                           'summary': (
                                     'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                           'title': (
                                   'django.db.models.fields.CharField', [], {'max_length': '216', 'null': 'True', 'blank': 'True'}), 
                           'url': (
                                 'django.db.models.fields.CharField', [], {'max_length': '216'})}, 
       'slideshow.slideshow': {'Meta': {'object_name': 'Slideshow', 'db_table': "'cmsplugin_slideshow'", '_ormbases': ['cms.CMSPlugin']}, 'cmsplugin_ptr': (
                                               'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'})}}
    complete_apps = [
     'slideshow']