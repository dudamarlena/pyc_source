# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/migrations/0008_auto_20200120_1735.py
# Compiled at: 2020-01-20 12:35:23
# Size of source mod 2**32: 576 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('translation_manager', '0007_auto_20170918_1731')]
    operations = [
     migrations.AlterField(model_name='remotetranslationentry',
       name='translation_entry',
       field=models.OneToOneField(on_delete=(django.db.models.deletion.PROTECT), related_name='remote_translation_entry', to='translation_manager.TranslationEntry'))]