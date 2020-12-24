# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/apps/django-testimony/testimony/migrations/0001_initial.py
# Compiled at: 2013-04-29 14:37:24
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('testimony_testimonial', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'author', self.gf('django.db.models.fields.CharField')(max_length=100)),
         (
          'position', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
         (
          'company', self.gf('django.db.models.fields.CharField')(max_length=100)),
         (
          'testimony', self.gf('django.db.models.fields.TextField')()),
         (
          'published', self.gf('django.db.models.fields.BooleanField')(default=False))))
        db.send_create_signal('testimony', ['Testimonial'])
        db.create_table('cmsplugin_testimonialplugin', (
         (
          'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
         (
          'block', self.gf('django.db.models.fields.CharField')(max_length=200)),
         (
          'size', self.gf('django.db.models.fields.IntegerField')()),
         (
          'list_type', self.gf('django.db.models.fields.CharField')(default='random', max_length=10)),
         (
          'template_path', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True))))
        db.send_create_signal('testimony', ['TestimonialPlugin'])

    def backwards(self, orm):
        db.delete_table('testimony_testimonial')
        db.delete_table('cmsplugin_testimonialplugin')

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
       'testimony.testimonial': {'Meta': {'ordering': "['author']", 'object_name': 'Testimonial'}, 'author': (
                                          'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                 'company': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                 'id': (
                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                 'position': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}), 
                                 'published': (
                                             'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                 'testimony': (
                                             'django.db.models.fields.TextField', [], {})}, 
       'testimony.testimonialplugin': {'Meta': {'object_name': 'TestimonialPlugin', 'db_table': "'cmsplugin_testimonialplugin'", '_ormbases': ['cms.CMSPlugin']}, 'block': (
                                               'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                                       'cmsplugin_ptr': (
                                                       'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                                       'list_type': (
                                                   'django.db.models.fields.CharField', [], {'default': "'random'", 'max_length': '10'}), 
                                       'size': (
                                              'django.db.models.fields.IntegerField', [], {}), 
                                       'template_path': (
                                                       'django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})}}
    complete_apps = [
     'testimony']