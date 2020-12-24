# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/faq/migrations/0002_auto__chg_field_question_question.py
# Compiled at: 2014-03-27 06:14:42
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.alter_column('faq_question', 'question', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):
        db.alter_column('faq_question', 'question', self.gf('django.db.models.fields.TextField')())

    models = {'faq.category': {'Meta': {'ordering': "['order', 'title']", 'object_name': 'Category'}, 'id': (
                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                        'order': (
                                'django.db.models.fields.IntegerField', [], {'default': '0'}), 
                        'title': (
                                'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'faq.question': {'Meta': {'ordering': "['order', 'question']", 'object_name': 'Question'}, 'active': (
                                 'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                        'answer': (
                                 'django.db.models.fields.TextField', [], {}), 
                        'category': (
                                   'django.db.models.fields.related.ForeignKey', [], {'to': "orm['faq.Category']"}), 
                        'created_at': (
                                     'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                        'id': (
                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                        'order': (
                                'django.db.models.fields.IntegerField', [], {'default': '0'}), 
                        'question': (
                                   'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                        'updated_at': (
                                     'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}}
    complete_apps = [
     'faq']