# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/apps/django-testimony/testimony/migrations/0002_auto__add_testimonialproduct__add_field_testimonialplugin_product__del.py
# Compiled at: 2014-01-10 19:11:55
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('testimony_testimonialproduct', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=100))))
        db.send_create_signal('testimony', ['TestimonialProduct'])
        db.add_column('cmsplugin_testimonialplugin', 'product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testimony.TestimonialProduct'], null=True, blank=True), keep_default=False)
        db.delete_column('testimony_testimonial', 'company')
        db.delete_column('testimony_testimonial', 'position')
        db.add_column('testimony_testimonial', 'product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testimony.TestimonialProduct'], null=True, blank=True), keep_default=False)

    def backwards(self, orm):
        db.delete_table('testimony_testimonialproduct')
        db.delete_column('cmsplugin_testimonialplugin', 'product_id')
        raise RuntimeError("Cannot reverse this migration. 'Testimonial.company' and its values cannot be restored.")
        db.add_column('testimony_testimonial', 'company', self.gf('django.db.models.fields.CharField')(max_length=100), keep_default=False)
        db.add_column('testimony_testimonial', 'position', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)
        db.delete_column('testimony_testimonial', 'product_id')

    models = {'cms.cmsplugin': {'Meta': {'object_name': 'CMSPlugin'}, 'changed_date': (
                                        'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                         'creation_date': (
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
                                 'id': (
                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                 'product': (
                                           'django.db.models.fields.related.ForeignKey', [], {'to': "orm['testimony.TestimonialProduct']", 'null': 'True', 'blank': 'True'}), 
                                 'published': (
                                             'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                 'testimony': (
                                             'django.db.models.fields.TextField', [], {})}, 
       'testimony.testimonialplugin': {'Meta': {'object_name': 'TestimonialPlugin', 'db_table': "u'cmsplugin_testimonialplugin'", '_ormbases': ['cms.CMSPlugin']}, 'block': (
                                               'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                                       'cmsplugin_ptr': (
                                                       'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                                       'list_type': (
                                                   'django.db.models.fields.CharField', [], {'default': "'random'", 'max_length': '10'}), 
                                       'product': (
                                                 'django.db.models.fields.related.ForeignKey', [], {'to': "orm['testimony.TestimonialProduct']", 'null': 'True', 'blank': 'True'}), 
                                       'size': (
                                              'django.db.models.fields.IntegerField', [], {}), 
                                       'template_path': (
                                                       'django.db.models.fields.CharField', [], {'default': "('testimony/list_default.html', 'Default list (stationary)')", 'max_length': '100'})}, 
       'testimony.testimonialproduct': {'Meta': {'ordering': "['name']", 'object_name': 'TestimonialProduct'}, 'id': (
                                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                        'name': (
                                               'django.db.models.fields.CharField', [], {'max_length': '100'})}}
    complete_apps = [
     'testimony']