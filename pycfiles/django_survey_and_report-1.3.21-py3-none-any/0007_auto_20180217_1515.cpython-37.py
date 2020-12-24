# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/migrations/0007_auto_20180217_1515.py
# Compiled at: 2019-03-02 04:44:34
# Size of source mod 2**32: 872 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('survey', '0006_add_related_name_for_categories')]
    operations = [
     migrations.AlterField(model_name='question',
       name='type',
       field=models.CharField(choices=[
      ('text', 'text (multiple line)'),
      ('short-text', 'short text (one line)'),
      ('radio', 'radio'),
      ('select', 'select'),
      ('select-multiple', 'Select Multiple'),
      ('select_image', 'Select Image'),
      ('integer', 'integer')],
       default='text',
       max_length=200))]