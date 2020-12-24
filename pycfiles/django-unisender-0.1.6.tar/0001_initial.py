# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/africa/work/python/dev_unisender/unisender/migrations/0001_initial.py
# Compiled at: 2014-07-08 04:12:47
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('unisender_tag', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'unisender_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'last_error', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'sync', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=255))))
        db.send_create_signal('unisender', ['Tag'])
        db.create_table('unisender_field', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'unisender_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'last_error', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'sync', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'field_type', self.gf('django.db.models.fields.CharField')(default='string', max_length=50)),
         (
          'visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
         (
          'sort', self.gf('django.db.models.fields.SmallIntegerField')(default=1))))
        db.send_create_signal('unisender', ['Field'])
        db.create_table('unisender_subscribelist', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'unisender_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'last_error', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'sync', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
         (
          'before_subscribe_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'after_subscribe_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True))))
        db.send_create_signal('unisender', ['SubscribeList'])
        db.create_table('unisender_subscriber', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'unisender_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'last_error', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'sync', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'contact_type', self.gf('django.db.models.fields.CharField')(default='email', max_length=50)),
         (
          'contact', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'double_optin', self.gf('django.db.models.fields.SmallIntegerField')(default=1))))
        db.send_create_signal('unisender', ['Subscriber'])
        m2m_table_name = db.shorten_name('unisender_subscriber_list_ids')
        db.create_table(m2m_table_name, (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'subscriber', models.ForeignKey(orm['unisender.subscriber'], null=False)),
         (
          'subscribelist', models.ForeignKey(orm['unisender.subscribelist'], null=False))))
        db.create_unique(m2m_table_name, ['subscriber_id', 'subscribelist_id'])
        m2m_table_name = db.shorten_name('unisender_subscriber_tags')
        db.create_table(m2m_table_name, (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'subscriber', models.ForeignKey(orm['unisender.subscriber'], null=False)),
         (
          'tag', models.ForeignKey(orm['unisender.tag'], null=False))))
        db.create_unique(m2m_table_name, ['subscriber_id', 'tag_id'])
        db.create_table('unisender_subscriberfields', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'subscriber', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fields', to=orm['unisender.Subscriber'])),
         (
          'field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['unisender.Field'])),
         (
          'value', self.gf('django.db.models.fields.CharField')(max_length=255))))
        db.send_create_signal('unisender', ['SubscriberFields'])
        db.create_table('unisender_emailmessage', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'unisender_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'last_error', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'sync', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'sender_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'sender_email', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'body', self.gf('tinymce_4.fields.TinyMCEModelField')()),
         (
          'list_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emails', to=orm['unisender.SubscribeList'])),
         (
          'tag', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='emails', null=True, to=orm['unisender.Tag'])),
         (
          'lang', self.gf('django.db.models.fields.CharField')(default='ru', max_length=50)),
         (
          'text_body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
         (
          'generate_text', self.gf('django.db.models.fields.CharField')(default='1', max_length=50)),
         (
          'wrap_type', self.gf('django.db.models.fields.CharField')(default='skip', max_length=50)),
         (
          'categories', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'series_day', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
         (
          'series_time', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2014, 7, 8, 0, 0)))))
        db.send_create_signal('unisender', ['EmailMessage'])
        db.create_table('unisender_smsmessage', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'unisender_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'last_error', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'sync', self.gf('django.db.models.fields.BooleanField')(default=False))))
        db.send_create_signal('unisender', ['SmsMessage'])
        db.create_table('unisender_campaign', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'unisender_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'last_error', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'sync', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'email_message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['unisender.EmailMessage'])),
         (
          'start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
         (
          'track_read', self.gf('django.db.models.fields.CharField')(default='0', max_length=50)),
         (
          'track_links', self.gf('django.db.models.fields.CharField')(default='0', max_length=50)),
         (
          'track_ga', self.gf('django.db.models.fields.CharField')(default='0', max_length=50)),
         (
          'payment_limit', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
         (
          'status', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
         (
          'last_check', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
         (
          'not_sent', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'ok_delivered', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'ok_read', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'ok_spam_folder', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'ok_link_visited', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'ok_unsubscribed', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_user_unknown', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_user_inactive', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_mailbox_full', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_spam_rejected', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_spam_folder', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_delivery_failed', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_will_retry', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_resend', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_domain_inactive', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_skip_letter', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_spam_skipped', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_spam_retry', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_unsubscribed', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_src_invalid', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_dest_invalid', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_not_allowed', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_not_available', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_lost', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'err_internal', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
         (
          'total', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0))))
        db.send_create_signal('unisender', ['Campaign'])
        m2m_table_name = db.shorten_name('unisender_campaign_contacts')
        db.create_table(m2m_table_name, (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'campaign', models.ForeignKey(orm['unisender.campaign'], null=False)),
         (
          'subscriber', models.ForeignKey(orm['unisender.subscriber'], null=False))))
        db.create_unique(m2m_table_name, ['campaign_id', 'subscriber_id'])
        return

    def backwards(self, orm):
        db.delete_table('unisender_tag')
        db.delete_table('unisender_field')
        db.delete_table('unisender_subscribelist')
        db.delete_table('unisender_subscriber')
        db.delete_table(db.shorten_name('unisender_subscriber_list_ids'))
        db.delete_table(db.shorten_name('unisender_subscriber_tags'))
        db.delete_table('unisender_subscriberfields')
        db.delete_table('unisender_emailmessage')
        db.delete_table('unisender_smsmessage')
        db.delete_table('unisender_campaign')
        db.delete_table(db.shorten_name('unisender_campaign_contacts'))

    models = {'unisender.campaign': {'Meta': {'ordering': "('name',)", 'object_name': 'Campaign'}, 'contacts': (
                                         'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'campaign'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['unisender.Subscriber']"}), 
                              'email_message': (
                                              'django.db.models.fields.related.ForeignKey', [], {'to': "orm['unisender.EmailMessage']"}), 
                              'err_delivery_failed': (
                                                    'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_dest_invalid': (
                                                 'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_domain_inactive': (
                                                    'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_internal': (
                                             'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_lost': (
                                         'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_mailbox_full': (
                                                 'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_not_allowed': (
                                                'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_not_available': (
                                                  'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_resend': (
                                           'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_skip_letter': (
                                                'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_spam_folder': (
                                                'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_spam_rejected': (
                                                  'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_spam_retry': (
                                               'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_spam_skipped': (
                                                 'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_src_invalid': (
                                                'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_unsubscribed': (
                                                 'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_user_inactive': (
                                                  'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_user_unknown': (
                                                 'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'err_will_retry': (
                                               'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'id': (
                                   'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                              'last_check': (
                                           'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                              'last_error': (
                                           'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                              'name': (
                                     'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                              'not_sent': (
                                         'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'ok_delivered': (
                                             'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'ok_link_visited': (
                                                'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'ok_read': (
                                        'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'ok_spam_folder': (
                                               'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'ok_unsubscribed': (
                                                'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'payment_limit': (
                                              'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                              'start_time': (
                                           'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                              'status': (
                                       'django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}), 
                              'sync': (
                                     'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                              'total': (
                                      'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                              'track_ga': (
                                         'django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '50'}), 
                              'track_links': (
                                            'django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '50'}), 
                              'track_read': (
                                           'django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '50'}), 
                              'unisender_id': (
                                             'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})}, 
       'unisender.emailmessage': {'Meta': {'ordering': "('subject',)", 'object_name': 'EmailMessage'}, 'body': (
                                         'tinymce_4.fields.TinyMCEModelField', [], {}), 
                                  'categories': (
                                               'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                  'generate_text': (
                                                  'django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '50'}), 
                                  'id': (
                                       'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                  'lang': (
                                         'django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '50'}), 
                                  'last_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 'list_id': (
                                            'django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'to': "orm['unisender.SubscribeList']"}), 
                                  'sender_email': (
                                                 'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                                  'sender_name': (
                                                'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                                  'series_day': (
                                               'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                                  'series_time': (
                                                'django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2014, 7, 8, 0, 0)'}), 
                                  'subject': (
                                            'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                                  'sync': (
                                         'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                  'tag': (
                                        'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'emails'", 'null': 'True', 'to': "orm['unisender.Tag']"}), 
                                  'text_body': (
                                              'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                                  'unisender_id': (
                                                 'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                  'wrap_type': (
                                              'django.db.models.fields.CharField', [], {'default': "'skip'", 'max_length': '50'})}, 
       'unisender.field': {'Meta': {'ordering': "('name',)", 'object_name': 'Field'}, 'field_type': (
                                        'django.db.models.fields.CharField', [], {'default': "'string'", 'max_length': '50'}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'last_error': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                           'name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                           'sort': (
                                  'django.db.models.fields.SmallIntegerField', [], {'default': '1'}), 
                           'sync': (
                                  'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                           'unisender_id': (
                                          'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                           'visible': (
                                     'django.db.models.fields.BooleanField', [], {'default': 'True'})}, 
       'unisender.smsmessage': {'Meta': {'object_name': 'SmsMessage'}, 'id': (
                                     'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                'last_error': (
                                             'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                'sync': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                'unisender_id': (
                                               'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})}, 
       'unisender.subscribelist': {'Meta': {'ordering': "('title',)", 'object_name': 'SubscribeList'}, 'after_subscribe_url': (
                                                         'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                   'before_subscribe_url': (
                                                          'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                   'id': (
                                        'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                   'last_error': (
                                                'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                   'sync': (
                                          'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                   'title': (
                                           'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}), 
                                   'unisender_id': (
                                                  'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})}, 
       'unisender.subscriber': {'Meta': {'ordering': "('contact',)", 'object_name': 'Subscriber'}, 'contact': (
                                          'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                                'contact_type': (
                                               'django.db.models.fields.CharField', [], {'default': "'email'", 'max_length': '50'}), 
                                'double_optin': (
                                               'django.db.models.fields.SmallIntegerField', [], {'default': '1'}), 
                                'id': (
                                     'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                'last_error': (
                                             'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                'list_ids': (
                                           'django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subscribers'", 'symmetrical': 'False', 'to': "orm['unisender.SubscribeList']"}), 
                                'sync': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                'tags': (
                                       'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'subscribers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['unisender.Tag']"}), 
                                'unisender_id': (
                                               'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})}, 
       'unisender.subscriberfields': {'Meta': {'object_name': 'SubscriberFields'}, 'field': (
                                              'django.db.models.fields.related.ForeignKey', [], {'to': "orm['unisender.Field']"}), 
                                      'id': (
                                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                      'subscriber': (
                                                   'django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': "orm['unisender.Subscriber']"}), 
                                      'value': (
                                              'django.db.models.fields.CharField', [], {'max_length': '255'})}, 
       'unisender.tag': {'Meta': {'ordering': "('name',)", 'object_name': 'Tag'}, 'id': (
                              'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'last_error': (
                                      'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                         'name': (
                                'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                         'sync': (
                                'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                         'unisender_id': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})}}
    complete_apps = [
     'unisender']