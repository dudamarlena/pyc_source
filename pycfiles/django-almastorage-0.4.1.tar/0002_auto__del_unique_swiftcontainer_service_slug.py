# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nurlan/private/work/alma.net/local/lib/python2.7/site-packages/almastorage/migrations/0002_auto__del_unique_swiftcontainer_service_slug.py
# Compiled at: 2015-08-19 01:48:23
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_unique('sw_container', ['service_slug'])

    def backwards(self, orm):
        db.create_unique('sw_container', ['service_slug'])

    models = {'alm_company.company': {'Meta': {'object_name': 'Company', 'db_table': "'alma_company'"}, 'date_created': (
                                              'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}), 
                               'date_edited': (
                                             'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}), 
                               'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'name': (
                                      'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                               'owner': (
                                       'django.db.models.fields.related.ManyToManyField', [], {'related_name': "'owned_company'", 'symmetrical': 'False', 'to': "orm['alm_user.User']"}), 
                               'subdomain': (
                                           'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'})}, 
       'alm_user.user': {'Meta': {'object_name': 'User', 'db_table': "'alma_user'"}, 'company': (
                                   'django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'symmetrical': 'False', 'to': "orm['alm_company.Company']"}), 
                         'date_created': (
                                        'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                         'date_edited': (
                                       'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                         'email': (
                                 'django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}), 
                         'first_name': (
                                      'django.db.models.fields.CharField', [], {'max_length': '31'}), 
                         'id': (
                              'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'is_active': (
                                     'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                         'is_admin': (
                                    'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                         'last_login': (
                                      'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                         'last_name': (
                                     'django.db.models.fields.CharField', [], {'max_length': '30'}), 
                         'password': (
                                    'django.db.models.fields.CharField', [], {'max_length': '128'}), 
                         'timezone': (
                                    'timezone_field.fields.TimeZoneField', [], {'default': "'Asia/Almaty'"}), 
                         'userpic_obj': (
                                       'django.db.models.fields.related.ForeignKey', [], {'default': '10', 'related_name': "'users'", 'null': 'True', 'blank': 'True', 'to': "orm['almastorage.SwiftFile']"}), 
                         'vcard': (
                                 'django.db.models.fields.related.OneToOneField', [], {'to': "orm['alm_vcard.VCard']", 'unique': 'True', 'null': 'True', 'blank': 'True'})}, 
       'alm_vcard.vcard': {'Meta': {'object_name': 'VCard', 'db_table': "'alma_vcard'"}, 'additional_name': (
                                             'django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}), 
                           'bday': (
                                  'django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}), 
                           'classP': (
                                    'django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}), 
                           'family_name': (
                                         'django.db.models.fields.CharField', [], {'max_length': '1024'}), 
                           'fn': (
                                'django.db.models.fields.CharField', [], {'max_length': '1024'}), 
                           'given_name': (
                                        'django.db.models.fields.CharField', [], {'max_length': '1024'}), 
                           'honorific_prefix': (
                                              'django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}), 
                           'honorific_suffix': (
                                              'django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'rev': (
                                 'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                           'sort_string': (
                                         'django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}), 
                           'uid': (
                                 'django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})}, 
       'almastorage.swiftcontainer': {'Meta': {'ordering': "['-date_created']", 'object_name': 'SwiftContainer', 'db_table': "'sw_container'"}, 'date_created': (
                                                     'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                      'id': (
                                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                      'service_slug': (
                                                     'django.db.models.fields.CharField', [], {'default': "'ALMASALES'", 'max_length': '30'}), 
                                      'title': (
                                              'django.db.models.fields.CharField', [], {'default': "'Main_container'", 'max_length': '255'})}, 
       'almastorage.swiftfile': {'Meta': {'ordering': "['-date_created']", 'object_name': 'SwiftFile', 'db_table': "'sw_file'"}, 'author': (
                                          'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'files_set'", 'null': 'True', 'to': "orm['alm_user.User']"}), 
                                 'container': (
                                             'django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['almastorage.SwiftContainer']"}), 
                                 'content_type': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                 'date_created': (
                                                'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                 'date_modified': (
                                                 'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 8, 19, 0, 0)', 'auto_now': 'True', 'blank': 'True'}), 
                                 'filename': (
                                            'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                                 'filesize': (
                                            'django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}), 
                                 'id': (
                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                 'key': (
                                       'django.db.models.fields.CharField', [], {'max_length': '40'}), 
                                 'temp_url': (
                                            'django.db.models.fields.CharField', [], {'max_length': '255'})}}
    complete_apps = [
     'almastorage']