# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/volunteer-coordination/volunteerhub/apps/volunteers/migrations/0003_auto__del_field_opportunity_fullfilled__add_field_opportunity_fulfille.py
# Compiled at: 2014-06-10 15:49:30
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_column('volunteers_opportunity', 'fullfilled')
        db.add_column('volunteers_opportunity', 'fulfilled', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

    def backwards(self, orm):
        db.add_column('volunteers_opportunity', 'fullfilled', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)
        db.delete_column('volunteers_opportunity', 'fulfilled')

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
       'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'custom_user.emailuser': {'Meta': {'object_name': 'EmailUser'}, 'date_joined': (
                                               'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                                 'email': (
                                         'django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}), 
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
                                 'password': (
                                            'django.db.models.fields.CharField', [], {'max_length': '128'}), 
                                 'user_permissions': (
                                                    'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"})}, 
       'volunteers.labortype': {'Meta': {'object_name': 'LaborType'}, 'description': (
                                              'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                                'id': (
                                     'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                'slug': (
                                       'django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}), 
                                'title': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255'})}, 
       'volunteers.location': {'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Location'}, 'address': (
                                         'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                               'city': (
                                      'django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}), 
                               'created': (
                                         'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                               'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'lat_long': (
                                          'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                               'modified': (
                                          'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                               'point': (
                                       'django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}), 
                               'slug': (
                                      'django.db.models.fields.SlugField', [], {'max_length': '50'}), 
                               'state': (
                                       'localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}), 
                               'zipcode': (
                                         'django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})}, 
       'volunteers.opportunity': {'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Opportunity'}, 'created': (
                                            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                                  'date': (
                                         'django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}), 
                                  'description': (
                                                'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                                  'fulfilled': (
                                              'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                  'id': (
                                       'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                  'labor_type': (
                                               'django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.LaborType']", 'null': 'True', 'blank': 'True'}), 
                                  'max_applicants': (
                                                   'django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}), 
                                  'modified': (
                                             'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                                  'project': (
                                            'django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Project']"}), 
                                  'slug': (
                                         'django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}), 
                                  'time': (
                                         'django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}), 
                                  'title': (
                                          'django.db.models.fields.CharField', [], {'max_length': '255'})}, 
       'volunteers.organization': {'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Organization'}, 'created': (
                                             'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                                   'description': (
                                                 'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                                   'id': (
                                        'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                   'managers': (
                                              'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['custom_user.EmailUser']", 'null': 'True', 'blank': 'True'}), 
                                   'modified': (
                                              'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                                   'phone': (
                                           'localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}), 
                                   'slug': (
                                          'django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}), 
                                   'title': (
                                           'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                                   'website': (
                                             'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})}, 
       'volunteers.project': {'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Project'}, 'created': (
                                        'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                              'description': (
                                            'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                              'id': (
                                   'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                              'image': (
                                      'django.db.models.fields.files.ImageField', [], {'max_length': '100'}), 
                              'lead_volunteers': (
                                                'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['custom_user.EmailUser']", 'null': 'True', 'blank': 'True'}), 
                              'modified': (
                                         'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                              'organization': (
                                             'django.db.models.fields.related.ForeignKey', [], {'related_name': "'organization'", 'to': "orm['volunteers.Organization']"}), 
                              'slug': (
                                     'django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}), 
                              'title': (
                                      'django.db.models.fields.CharField', [], {'max_length': '255'})}, 
       'volunteers.volunteer': {'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Volunteer'}, 'address': (
                                          'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                'created': (
                                          'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                                'id': (
                                     'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                'modified': (
                                           'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                                'name': (
                                       'django.db.models.fields.TextField', [], {'max_length': '255'}), 
                                'opportunities_completed': (
                                                          'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['volunteers.Opportunity']", 'null': 'True', 'blank': 'True'}), 
                                'phone_number': (
                                               'localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})}, 
       'volunteers.volunteerapplication': {'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'VolunteerApplication'}, 'created': (
                                                     'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                                           'id': (
                                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                           'modified': (
                                                      'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}), 
                                           'opportunity': (
                                                         'django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Opportunity']"}), 
                                           'status': (
                                                    'django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '15'}), 
                                           'volunteer': (
                                                       'django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Volunteer']"})}}
    complete_apps = [
     'volunteers']