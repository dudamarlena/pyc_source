# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0002_move_fields_to_form.py
# Compiled at: 2017-09-07 07:30:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('formfactory', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name=b'wizard', name=b'post_to'),
     migrations.RemoveField(model_name=b'wizard', name=b'submit_button_text'),
     migrations.AlterField(model_name=b'action', name=b'action', field=models.CharField(choices=[('formfactory.actions.login', 'formfactory.actions.login'), ('formfactory.actions.send_email', 'formfactory.actions.send_email'), ('formfactory.actions.store_data', 'formfactory.actions.store_data')], max_length=128)),
     migrations.AlterField(model_name=b'form', name=b'post_to', field=models.CharField(blank=True, help_text=b'URL to which this form will be posted to. Leave blank to                         post back to original view.', max_length=256, null=True)),
     migrations.AlterField(model_name=b'formfield', name=b'additional_validators', field=models.CharField(blank=True, max_length=128, null=True))]