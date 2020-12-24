# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nicp/nyaruka/tns-glass/tns_glass/rapidsms_httprouter/migrations/0002_auto__add_field_message_updated.py
# Compiled at: 2012-10-08 13:47:23
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('rapidsms_httprouter_message', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True), keep_default=False)

    def backwards(self, orm):
        db.delete_column('rapidsms_httprouter_message', 'updated')

    models = {'rapidsms.backend': {'Meta': {'object_name': 'Backend'}, 'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'name': (
                                   'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})}, 
       'rapidsms.connection': {'Meta': {'unique_together': "(('backend', 'identity'),)", 'object_name': 'Connection'}, 'backend': (
                                         'django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Backend']"}), 
                               'contact': (
                                         'django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Contact']", 'null': 'True', 'blank': 'True'}), 
                               'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'identity': (
                                          'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'rapidsms.contact': {'Meta': {'object_name': 'Contact'}, 'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'language': (
                                       'django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}), 
                            'name': (
                                   'django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})}, 
       'rapidsms_httprouter.message': {'Meta': {'object_name': 'Message'}, 'connection': (
                                                    'django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': "orm['rapidsms.Connection']"}), 
                                       'date': (
                                              'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                       'direction': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '1'}), 
                                       'id': (
                                            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                       'in_response_to': (
                                                        'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'responses'", 'null': 'True', 'to': "orm['rapidsms_httprouter.Message']"}), 
                                       'status': (
                                                'django.db.models.fields.CharField', [], {'max_length': '1'}), 
                                       'text': (
                                              'django.db.models.fields.TextField', [], {}), 
                                       'updated': (
                                                 'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})}}
    complete_apps = [
     'rapidsms_httprouter']