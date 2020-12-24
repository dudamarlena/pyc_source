# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/email_filter/migrations/0004_auto__add_field_emaillog_cc__add_field_emaillog_bcc.py
# Compiled at: 2014-07-02 06:59:14
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('email_filter_emaillog', 'cc', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=''), keep_default=False)
        db.add_column('email_filter_emaillog', 'bcc', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=''), keep_default=False)

    def backwards(self, orm):
        db.delete_column('email_filter_emaillog', 'cc')
        db.delete_column('email_filter_emaillog', 'bcc')

    models = {'email_filter.emailattachment': {'Meta': {'object_name': 'EmailAttachment'}, 'attachment': (
                                                     'django.db.models.fields.files.FileField', [], {'max_length': '100'}), 
                                        'email_log': (
                                                    'django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['email_filter.EmailLog']"}), 
                                        'id': (
                                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'})}, 
       'email_filter.emaillog': {'Meta': {'object_name': 'EmailLog'}, 'bcc': (
                                       'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': "''"}), 
                                 'cc': (
                                      'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': "''"}), 
                                 'created': (
                                           'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                 'id': (
                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                 'in_reply_to': (
                                               'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}), 
                                 'message_id': (
                                              'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}), 
                                 'raw_body': (
                                            'django.db.models.fields.TextField', [], {}), 
                                 'raw_email': (
                                             'django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}), 
                                 'recipient': (
                                             'django.db.models.fields.CharField', [], {'max_length': '750'}), 
                                 'sender': (
                                          'django.db.models.fields.EmailField', [], {'max_length': '250'}), 
                                 'sent': (
                                        'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                                 'subject': (
                                           'django.db.models.fields.CharField', [], {'max_length': '255'})}, 
       'email_filter.emailredirect': {'Meta': {'unique_together': "(('email_in', 'email_redirect'),)", 'object_name': 'EmailRedirect'}, 'email_in': (
                                                 'django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '250'}), 
                                      'email_redirect': (
                                                       'django.db.models.fields.EmailField', [], {'max_length': '250'}), 
                                      'id': (
                                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'})}}
    complete_apps = [
     'email_filter']