# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/insality/code/django/scibib/src/scibib/newsletter/migrations/0003_changing_mail_templates.py
# Compiled at: 2014-03-28 04:05:27
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        """Write your forwards methods here."""
        template_text = orm['newsletter.mailtemplate'].objects.get(name='Ежемесячная рассылка')
        template_text.template = '\n<b>Доброго времени суток!</b>\n<br>\n<i>На нашем сайте произошли следующие изменения:</i>\n<br>\n{{text}}\n<br>\n<i>С уважением, администрация сайта "{{res_name}}"</i>\n'
        template_text.save()
        template_text = orm['newsletter.mailtemplate'].objects.get(name='Пользовательское письмо')
        template_text.template = '\n<b>Доброго времени суток!</b>\n<br>\n<i>У нас есть для вас следующая информация:</i>\n<br>\n{{text}}\n<br>\n<i>С уважением, администрация сайта "{{res_name}}"</i>\n'
        template_text.save()

    def backwards(self, orm):
        """Write your backwards methods here."""
        template_text = orm['newsletter.mailtemplate'].objects.get(name='Ежемесячная рассылка')
        template_text.template = '\n<b>Доброго времени суток!</b>\n<br>\n<i>На нашем сайте произошли следующие изменения:</i>\n<br>\n{{text}}\n<br>\n<i>С уважением, администрация сайта SciBib</i>\n'
        template_text.save()
        template_text = orm['newsletter.mailtemplate'].objects.get(name='Пользовательское письмо')
        template_text.template = '\n<b>Доброго времени суток!</b>\n<br>\n<i>У нас есть для вас следующая информация:</i>\n<br>\n{{text}}\n<br>\n<i>С уважением, администрация сайта SciBib</i>\n'
        template_text.save()

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
    symmetrical = True