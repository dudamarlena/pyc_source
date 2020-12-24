# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0012_auto_20170703_1030.py
# Compiled at: 2017-11-28 02:57:16
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('formfactory', '0011_form_field_label_length_change')]
    operations = [
     migrations.AddField(model_name=b'form', name=b'ajax_post', field=models.BooleanField(default=False, help_text=b'Hook for default submit handler to be overriden by JS.', verbose_name=b'Enable AJAX posting.'))]