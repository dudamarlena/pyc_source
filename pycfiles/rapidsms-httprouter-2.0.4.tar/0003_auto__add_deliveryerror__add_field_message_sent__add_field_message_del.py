# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nicp/nyaruka/tns-glass/tns_glass/rapidsms_httprouter/migrations/0003_auto__add_deliveryerror__add_field_message_sent__add_field_message_del.py
# Compiled at: 2012-10-09 04:20:29
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('rapidsms_httprouter_deliveryerror', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='errors', to=orm['rapidsms_httprouter.Message'])),
         (
          'log', self.gf('django.db.models.fields.TextField')()),
         (
          'created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True))))
        db.send_create_signal('rapidsms_httprouter', ['DeliveryError'])
        db.add_column('rapidsms_httprouter_message', 'sent', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)
        db.add_column('rapidsms_httprouter_message', 'delivered', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

    def backwards(self, orm):
        db.delete_table('rapidsms_httprouter_deliveryerror')
        db.delete_column('rapidsms_httprouter_message', 'sent')
        db.delete_column('rapidsms_httprouter_message', 'delivered')

    models = {'rapidsms.backend': {'Meta': {'object_name': 'Backend'}, 'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'name': (
                                   'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})}, 
       'rapidsms.connection': {'Meta': {'object_name': 'Connection'}, 'backend': (
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
       'rapidsms_httprouter.deliveryerror': {'Meta': {'object_name': 'DeliveryError'}, 'created_on': (
                                                          'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                             'id': (
                                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                             'log': (
                                                   'django.db.models.fields.TextField', [], {}), 
                                             'message': (
                                                       'django.db.models.fields.related.ForeignKey', [], {'related_name': "'errors'", 'to': "orm['rapidsms_httprouter.Message']"})}, 
       'rapidsms_httprouter.message': {'Meta': {'object_name': 'Message'}, 'connection': (
                                                    'django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': "orm['rapidsms.Connection']"}), 
                                       'date': (
                                              'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                       'delivered': (
                                                   'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                                       'direction': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '1'}), 
                                       'id': (
                                            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                       'in_response_to': (
                                                        'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'responses'", 'null': 'True', 'to': "orm['rapidsms_httprouter.Message']"}), 
                                       'sent': (
                                              'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                                       'status': (
                                                'django.db.models.fields.CharField', [], {'max_length': '1'}), 
                                       'text': (
                                              'django.db.models.fields.TextField', [], {}), 
                                       'updated': (
                                                 'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})}}
    complete_apps = [
     'rapidsms_httprouter']