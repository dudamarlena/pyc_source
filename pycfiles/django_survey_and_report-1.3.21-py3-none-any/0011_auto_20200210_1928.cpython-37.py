# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/migrations/0011_auto_20200210_1928.py
# Compiled at: 2020-02-25 03:28:34
# Size of source mod 2**32: 1022 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('survey', '0010_survey_editable_answers')]
    operations = [
     migrations.AddField(model_name='survey',
       name='expire_date',
       field=models.DateField(blank=True, null=True, verbose_name='Validity')),
     migrations.AddField(model_name='survey', name='publish_date', field=models.DateField(auto_now=True)),
     migrations.AlterField(model_name='question',
       name='choices',
       field=models.TextField(blank=True,
       help_text="The choices field is only used if the question                 type\nif the question type is 'radio', 'select', or\n'select multiple'                     provide a comma-separated list of\noptions for this question .",
       null=True,
       verbose_name='Choices'))]