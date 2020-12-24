# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/migrations/0002_survey_template.py
# Compiled at: 2020-01-26 10:04:56
# Size of source mod 2**32: 333 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('survey', '0001_initial')]
    operations = [
     migrations.AddField(model_name='survey',
       name='template',
       field=models.CharField(max_length=255, null=True, blank=True))]