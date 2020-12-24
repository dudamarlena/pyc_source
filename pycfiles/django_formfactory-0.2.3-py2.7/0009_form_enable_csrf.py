# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0009_form_enable_csrf.py
# Compiled at: 2017-09-07 07:30:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('formfactory', '0008_custom_field_error_messages')]
    operations = [
     migrations.AddField(model_name=b'form', name=b'enable_csrf', field=models.BooleanField(default=True, help_text=b'Cross site request forgery protection may not be needed in all cases. Since it incurs a performance penalty you may wish to disable it.', verbose_name=b'Enable CSRF protection'))]