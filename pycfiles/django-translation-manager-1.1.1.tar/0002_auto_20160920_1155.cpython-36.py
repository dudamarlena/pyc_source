# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/migrations/0002_auto_20160920_1155.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 532 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('translation_manager', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='translationentry',
       name='language',
       field=models.CharField(db_index=True, max_length=7, verbose_name='admin-translation_entry-language-label'))]