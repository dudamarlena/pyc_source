# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/GitHub/django_sendgrid_repo/django_sendgrid_parse/migrations/0004_auto_20160816_1704.py
# Compiled at: 2016-08-21 23:09:38
# Size of source mod 2**32: 2773 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [
     ('django_sendgrid_parse', '0003_auto_20160730_0019')]
    operations = [
     migrations.AlterField(model_name='email', name='SPF', field=jsonfield.fields.JSONField(blank=True, null=True, verbose_name='Sender Policy Framework')),
     migrations.AlterField(model_name='email', name='cc', field=models.TextField(blank=True, null=True, verbose_name='Hidden')),
     migrations.AlterField(model_name='email', name='charsets', field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Charsets')),
     migrations.AlterField(model_name='email', name='dkim', field=jsonfield.fields.JSONField(blank=True, null=True, verbose_name='DomainKeys Identified Mail')),
     migrations.AlterField(model_name='email', name='envelope', field=jsonfield.fields.JSONField(blank=True, null=True, verbose_name='Envelope')),
     migrations.AlterField(model_name='email', name='from_mailbox', field=models.TextField(verbose_name='From')),
     migrations.AlterField(model_name='email', name='headers', field=models.TextField(blank=True, null=True, verbose_name='Headers')),
     migrations.AlterField(model_name='email', name='html', field=models.TextField(blank=True, null=True, verbose_name='HTML')),
     migrations.AlterField(model_name='email', name='spam_report', field=models.TextField(blank=True, null=True, verbose_name='Spam report')),
     migrations.AlterField(model_name='email', name='spam_score', field=models.FloatField(blank=True, null=True, verbose_name='Spam score')),
     migrations.AlterField(model_name='email', name='subject', field=models.TextField(blank=True, null=True, verbose_name='Carbon Copy')),
     migrations.AlterField(model_name='email', name='text', field=models.TextField(blank=True, null=True, verbose_name='Text')),
     migrations.AlterField(model_name='email', name='to_mailbox', field=models.TextField(verbose_name='To'))]