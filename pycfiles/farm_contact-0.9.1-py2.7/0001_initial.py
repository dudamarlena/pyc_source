# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/contact/migrations/0001_initial.py
# Compiled at: 2014-03-26 08:39:13
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('contact_enquirytype', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=255))))
        db.send_create_signal('contact', ['EnquiryType'])
        db.create_table('contact_enquiry', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
         (
          'phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'enquiry_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.EnquiryType'])),
         (
          'message', self.gf('django.db.models.fields.TextField')()),
         (
          'ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
         (
          'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))))
        db.send_create_signal('contact', ['Enquiry'])

    def backwards(self, orm):
        db.delete_table('contact_enquirytype')
        db.delete_table('contact_enquiry')

    models = {'contact.enquiry': {'Meta': {'object_name': 'Enquiry'}, 'created_at': (
                                        'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                           'email': (
                                   'django.db.models.fields.EmailField', [], {'max_length': '75'}), 
                           'enquiry_type': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.EnquiryType']"}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'ip': (
                                'django.db.models.fields.IPAddressField', [], {'max_length': '15'}), 
                           'message': (
                                     'django.db.models.fields.TextField', [], {}), 
                           'name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                           'phone': (
                                   'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                           'updated_at': (
                                        'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}, 
       'contact.enquirytype': {'Meta': {'object_name': 'EnquiryType'}, 'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'name': (
                                      'django.db.models.fields.CharField', [], {'max_length': '255'})}}
    complete_apps = [
     'contact']