# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/GitHub/django_sendgrid_repo/django_sendgrid_parse/migrations/0005_auto_20160816_1919.py
# Compiled at: 2016-08-21 23:09:38
# Size of source mod 2**32: 1404 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_sendgrid_parse', '0004_auto_20160816_1704')]
    operations = [
     migrations.AlterField(model_name='email', name='SPF', field=models.TextField(blank=True, null=True, verbose_name='Sender Policy Framework')),
     migrations.AlterField(model_name='email', name='cc', field=models.TextField(blank=True, null=True, verbose_name='Carbon Copy')),
     migrations.AlterField(model_name='email', name='dkim', field=models.TextField(blank=True, null=True, verbose_name='DomainKeys Identified Mail')),
     migrations.AlterField(model_name='email', name='from_mailbox', field=models.TextField(verbose_name='From^')),
     migrations.AlterField(model_name='email', name='subject', field=models.TextField(blank=True, null=True, verbose_name='Subject')),
     migrations.AlterField(model_name='email', name='to_mailbox', field=models.TextField(verbose_name='To^'))]