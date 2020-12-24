# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leotrubach/development/django-saas-email/venv/lib/python3.7/site-packages/django_saas_email/migrations/0006_add_to_and_from_names.py
# Compiled at: 2019-02-24 06:44:41
# Size of source mod 2**32: 715 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_saas_email', '0005_mail_bcc_address')]
    operations = [
     migrations.AddField(model_name='mail',
       name='from_name',
       field=models.CharField(blank=True, help_text='Email sender name', max_length=100, null=True, verbose_name='Sender name')),
     migrations.AddField(model_name='mail',
       name='to_name',
       field=models.CharField(blank=True, help_text='Email recipient name', max_length=100, null=True, verbose_name='Recipient name'))]