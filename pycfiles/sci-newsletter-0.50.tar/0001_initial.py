# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/insality/code/django/scibib/src/scibib/newsletter/migrations/0001_initial.py
# Compiled at: 2014-03-27 07:11:50
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('newsletter_newslettersettings', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'newsletter_type', self.gf('django.db.models.fields.CharField')(default='0', max_length=125)),
         (
          'day', self.gf('django.db.models.fields.IntegerField')(default=7))))
        db.send_create_signal('newsletter', ['NewsletterSettings'])
        db.create_table('newsletter_job', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'send_date', self.gf('django.db.models.fields.DateField')()),
         (
          'state', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=1, decimal_places=0)),
         (
          'mail', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mails', to=orm['newsletter.Mail'])),
         (
          'recievers', self.gf('django.db.models.fields.CharField')(default='0', max_length=125))))
        db.send_create_signal('newsletter', ['Job'])
        db.create_table('newsletter_mail', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'subject', self.gf('django.db.models.fields.CharField')(max_length=125)),
         (
          'text', self.gf('ckeditor.fields.RichTextField')()),
         (
          'template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='templates', to=orm['newsletter.MailTemplate']))))
        db.send_create_signal('newsletter', ['Mail'])
        db.create_table('newsletter_mailtemplate', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=125)),
         (
          'template', self.gf('django.db.models.fields.TextField')())))
        db.send_create_signal('newsletter', ['MailTemplate'])

    def backwards(self, orm):
        db.delete_table('newsletter_newslettersettings')
        db.delete_table('newsletter_job')
        db.delete_table('newsletter_mail')
        db.delete_table('newsletter_mailtemplate')

    models = {'newsletter.job': {'Meta': {'object_name': 'Job'}, 'id': (
                               'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                          'mail': (
                                 'django.db.models.fields.related.ForeignKey', [], {'related_name': "'mails'", 'to': "orm['newsletter.Mail']"}), 
                          'recievers': (
                                      'django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '125'}), 
                          'send_date': (
                                      'django.db.models.fields.DateField', [], {}), 
                          'state': (
                                  'django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '1', 'decimal_places': '0'})}, 
       'newsletter.mail': {'Meta': {'object_name': 'Mail'}, 'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'subject': (
                                     'django.db.models.fields.CharField', [], {'max_length': '125'}), 
                           'template': (
                                      'django.db.models.fields.related.ForeignKey', [], {'related_name': "'templates'", 'to': "orm['newsletter.MailTemplate']"}), 
                           'text': (
                                  'ckeditor.fields.RichTextField', [], {})}, 
       'newsletter.mailtemplate': {'Meta': {'object_name': 'MailTemplate'}, 'id': (
                                        'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                   'name': (
                                          'django.db.models.fields.CharField', [], {'max_length': '125'}), 
                                   'template': (
                                              'django.db.models.fields.TextField', [], {})}, 
       'newsletter.newslettersettings': {'Meta': {'object_name': 'NewsletterSettings'}, 'day': (
                                               'django.db.models.fields.IntegerField', [], {'default': '7'}), 
                                         'id': (
                                              'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                         'newsletter_type': (
                                                           'django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '125'})}}
    complete_apps = [
     'newsletter']