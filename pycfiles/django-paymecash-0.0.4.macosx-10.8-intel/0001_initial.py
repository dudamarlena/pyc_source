# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-paymecash/example/../paymecash/migrations/0001_initial.py
# Compiled at: 2013-09-17 04:23:07
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('paymecash_payment', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'order_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
         (
          'wallet_id', self.gf('django.db.models.fields.PositiveIntegerField')(default='000000001060')),
         (
          'product_price', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
         (
          'product_currency', self.gf('django.db.models.fields.CharField')(default='RUB', max_length=3)),
         (
          'payment_type_group_id', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, null=True, blank=True)),
         (
          'cs1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'cs2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'cs3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'result', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
         (
          'transaction_id', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
         (
          'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
         (
          'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True))))
        db.send_create_signal('paymecash', ['Payment'])

    def backwards(self, orm):
        db.delete_table('paymecash_payment')

    models = {'paymecash.payment': {'Meta': {'ordering': "('created',)", 'object_name': 'Payment'}, 'created': (
                                       'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                             'cs1': (
                                   'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                             'cs2': (
                                   'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                             'cs3': (
                                   'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                             'id': (
                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                             'order_id': (
                                        'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}), 
                             'payment_type_group_id': (
                                                     'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}), 
                             'product_currency': (
                                                'django.db.models.fields.CharField', [], {'default': "'RUB'", 'max_length': '3'}), 
                             'product_price': (
                                             'django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}), 
                             'result': (
                                      'django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}), 
                             'transaction_id': (
                                              'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                             'updated': (
                                       'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                             'wallet_id': (
                                         'django.db.models.fields.PositiveIntegerField', [], {'default': "'000000001060'"})}}
    complete_apps = [
     'paymecash']