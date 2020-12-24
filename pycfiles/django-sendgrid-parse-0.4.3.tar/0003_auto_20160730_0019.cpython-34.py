# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/GitHub/django_sendgrid_repo/django_sendgrid_parse/migrations/0003_auto_20160730_0019.py
# Compiled at: 2016-08-21 23:09:38
# Size of source mod 2**32: 1245 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, django_sendgrid_parse.models

class Migration(migrations.Migration):
    dependencies = [
     ('django_sendgrid_parse', '0002_auto_20160729_1816')]
    operations = [
     migrations.RemoveField(model_name='email', name='attachments'),
     migrations.AddField(model_name='attachment', name='email', field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='django_sendgrid_parse.Email', verbose_name='Email Attached To'), preserve_default=False),
     migrations.AddField(model_name='attachment', name='number', field=models.IntegerField(default=1, verbose_name="Email's Attachment Number")),
     migrations.AlterField(model_name='attachment', name='file', field=models.FileField(upload_to=django_sendgrid_parse.models.attachments_file_upload, verbose_name='Attached File'))]