# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0003_formfieldgroup_show_title.py
# Compiled at: 2017-09-07 07:30:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('formfactory', '0002_move_fields_to_form')]
    operations = [
     migrations.AddField(model_name=b'formfieldgroup', name=b'show_title', field=models.BooleanField(default=False, help_text=b'Select this for Field group title to be displayed.'))]