# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/migrations/0012_auto_20200224_2220.py
# Compiled at: 2020-02-25 03:28:34
# Size of source mod 2**32: 1350 bytes
import datetime
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('survey', '0011_auto_20200210_1928')]
    operations = [
     migrations.AlterField(model_name='question',
       name='choices',
       field=models.TextField(blank=True,
       help_text="The choices field is only used if the question type\nif the question type is 'radio', 'select', or\n'select multiple' provide a comma-separated list of\noptions for this question .",
       null=True,
       verbose_name='Choices')),
     migrations.AlterField(model_name='survey',
       name='expire_date',
       field=models.DateField(blank=True, default=(datetime.date(2020, 3, 2)), verbose_name='Expiration date')),
     migrations.AlterField(model_name='survey',
       name='is_published',
       field=models.BooleanField(default=True, verbose_name='Users can see it and answer it')),
     migrations.AlterField(model_name='survey',
       name='publish_date',
       field=models.DateField(blank=True, default=(datetime.date(2020, 2, 24)), verbose_name='Publication date'))]