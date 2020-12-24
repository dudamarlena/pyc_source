# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leotrubach/development/django-saas-email/venv/lib/python3.7/site-packages/django_saas_email/migrations/0005_mail_bcc_address.py
# Compiled at: 2019-01-21 07:54:01
# Size of source mod 2**32: 495 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_saas_email', '0004_mail_cc_address')]
    operations = [
     migrations.AddField(model_name='mail',
       name='bcc_address',
       field=models.EmailField(blank=True, help_text="The 'bcc' field of the email", max_length=254, null=True, verbose_name='BCC email address'))]