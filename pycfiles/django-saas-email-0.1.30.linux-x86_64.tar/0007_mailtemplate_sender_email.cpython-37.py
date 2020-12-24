# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leotrubach/development/django-saas-email/venv/lib/python3.7/site-packages/django_saas_email/migrations/0007_mailtemplate_sender_email.py
# Compiled at: 2019-03-28 10:39:18
# Size of source mod 2**32: 545 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_saas_email', '0006_add_to_and_from_names')]
    operations = [
     migrations.AddField(model_name='mailtemplate',
       name='sender_email',
       field=models.EmailField(blank=True, help_text='Email to use as sender address when the template is used. If not set then default address is used', max_length=254, null=True))]