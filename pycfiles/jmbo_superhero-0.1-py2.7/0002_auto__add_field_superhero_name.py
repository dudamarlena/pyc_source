# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superhero/migrations/0002_auto__add_field_superhero_name.py
# Compiled at: 2015-05-05 00:01:33
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('superhero_superhero', 'name', self.gf('django.db.models.fields.CharField')(default='legacy', max_length=256), keep_default=False)

    def backwards(self, orm):
        db.delete_column('superhero_superhero', 'name')

    models = {'auth.group': {'Meta': {'object_name': 'Group'}, 'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}), 
                      'permissions': (
                                    'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})}, 
       'auth.permission': {'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'}, 'codename': (
                                      'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                           'content_type': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '50'})}, 
       'auth.user': {'Meta': {'object_name': 'User'}, 'date_joined': (
                                   'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                     'email': (
                             'django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}), 
                     'first_name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}), 
                     'groups': (
                              'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}), 
                     'id': (
                          'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                     'is_active': (
                                 'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                     'is_staff': (
                                'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                     'is_superuser': (
                                    'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                     'last_login': (
                                  'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                     'last_name': (
                                 'django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}), 
                     'password': (
                                'django.db.models.fields.CharField', [], {'max_length': '128'}), 
                     'user_permissions': (
                                        'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}), 
                     'username': (
                                'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})}, 
       'category.category': {'Meta': {'ordering': "('title',)", 'object_name': 'Category'}, 'id': (
                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                             'parent': (
                                      'django.db.models.fields.related.ForeignKey', [], {'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}), 
                             'sites': (
                                     'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}), 
                             'slug': (
                                    'django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}), 
                             'subtitle': (
                                        'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                             'title': (
                                     'django.db.models.fields.CharField', [], {'max_length': '200'})}, 
       'category.tag': {'Meta': {'ordering': "('title',)", 'object_name': 'Tag'}, 'categories': (
                                     'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}), 
                        'id': (
                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                        'slug': (
                               'django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}), 
                        'title': (
                                'django.db.models.fields.CharField', [], {'max_length': '200'})}, 
       'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'jmbo.modelbase': {'Meta': {'ordering': "('-publish_on', '-created')", 'object_name': 'ModelBase'}, 'anonymous_comments': (
                                               'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                          'anonymous_likes': (
                                            'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                          'categories': (
                                       'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}), 
                          'class_name': (
                                       'django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}), 
                          'comment_count': (
                                          'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                          'comments_closed': (
                                            'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                          'comments_enabled': (
                                             'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                          'content_type': (
                                         'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}), 
                          'created': (
                                    'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}), 
                          'crop_from': (
                                      'django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}), 
                          'date_taken': (
                                       'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                          'description': (
                                        'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                          'effect': (
                                   'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'modelbase_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}), 
                          'id': (
                               'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                          'image': (
                                  'django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}), 
                          'image_attribution': (
                                              'django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}), 
                          'likes_closed': (
                                         'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                          'likes_enabled': (
                                          'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                          'modified': (
                                     'django.db.models.fields.DateTimeField', [], {'db_index': 'True'}), 
                          'owner': (
                                  'django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}), 
                          'owner_override': (
                                           'django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}), 
                          'primary_category': (
                                             'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary_modelbase_set'", 'null': 'True', 'to': "orm['category.Category']"}), 
                          'publish_on': (
                                       'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                          'publishers': (
                                       'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['publisher.Publisher']", 'null': 'True', 'blank': 'True'}), 
                          'retract_on': (
                                       'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                          'sites': (
                                  'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}), 
                          'slug': (
                                 'django.db.models.fields.SlugField', [], {'max_length': '255'}), 
                          'state': (
                                  'django.db.models.fields.CharField', [], {'default': "'unpublished'", 'max_length': '32', 'null': 'True', 'blank': 'True'}), 
                          'subtitle': (
                                     'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                          'tags': (
                                 'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Tag']", 'null': 'True', 'blank': 'True'}), 
                          'title': (
                                  'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                          'view_count': (
                                       'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                          'vote_total': (
                                       'django.db.models.fields.PositiveIntegerField', [], {'default': '0'})}, 
       'photologue.photoeffect': {'Meta': {'object_name': 'PhotoEffect'}, 'background_color': (
                                                     'django.db.models.fields.CharField', [], {'default': "'#FFFFFF'", 'max_length': '7'}), 
                                  'brightness': (
                                               'django.db.models.fields.FloatField', [], {'default': '1.0'}), 
                                  'color': (
                                          'django.db.models.fields.FloatField', [], {'default': '1.0'}), 
                                  'contrast': (
                                             'django.db.models.fields.FloatField', [], {'default': '1.0'}), 
                                  'description': (
                                                'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                                  'filters': (
                                            'django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}), 
                                  'id': (
                                       'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                  'name': (
                                         'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}), 
                                  'reflection_size': (
                                                    'django.db.models.fields.FloatField', [], {'default': '0'}), 
                                  'reflection_strength': (
                                                        'django.db.models.fields.FloatField', [], {'default': '0.6'}), 
                                  'sharpness': (
                                              'django.db.models.fields.FloatField', [], {'default': '1.0'}), 
                                  'transpose_method': (
                                                     'django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})}, 
       'publisher.publisher': {'Meta': {'object_name': 'Publisher'}, 'class_name': (
                                            'django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}), 
                               'content_type': (
                                              'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}), 
                               'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'title': (
                                       'django.db.models.fields.CharField', [], {'max_length': '64'})}, 
       'sites.site': {'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"}, 'domain': (
                               'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                      'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'max_length': '50'})}, 
       'superhero.superhero': {'Meta': {'ordering': "('-publish_on', '-created')", 'object_name': 'Superhero', '_ormbases': ['jmbo.ModelBase']}, 'modelbase_ptr': (
                                               'django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}), 
                               'name': (
                                      'django.db.models.fields.CharField', [], {'max_length': '256'})}}
    complete_apps = [
     'superhero']