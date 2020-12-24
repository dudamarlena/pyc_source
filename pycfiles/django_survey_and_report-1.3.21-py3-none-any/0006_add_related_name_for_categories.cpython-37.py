# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/migrations/0006_add_related_name_for_categories.py
# Compiled at: 2020-01-26 10:04:56
# Size of source mod 2**32: 548 bytes
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('survey', '0005_rename_question_related_name')]
    operations = [
     migrations.AlterField(model_name='category',
       name='survey',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
       related_name='categories',
       to='survey.Survey'))]