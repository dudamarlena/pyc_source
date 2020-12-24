# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/migrations/0003_auto_20170320_0337.py
# Compiled at: 2020-01-26 10:04:57
# Size of source mod 2**32: 2375 bytes
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('survey', '0002_survey_template')]
    operations = [
     migrations.RenameField(model_name='question', old_name='question_type', new_name='type'),
     migrations.AddField(model_name='category',
       name='description',
       field=models.CharField(blank=True, max_length=2000, null=True)),
     migrations.AlterField(model_name='answerbase',
       name='question',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
       related_name='answers',
       to='survey.Question')),
     migrations.AlterField(model_name='answerbase',
       name='response',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
       related_name='answers',
       to='survey.Response')),
     migrations.AlterField(model_name='question',
       name='category',
       field=models.ForeignKey(blank=True,
       null=True,
       on_delete=(django.db.models.deletion.CASCADE),
       related_name='related_questions',
       to='survey.Category')),
     migrations.AlterField(model_name='question',
       name='choices',
       field=models.TextField(blank=True,
       help_text="The choices field is only used if the question type\nif the question type is 'radio', 'select', or\n'select multiple' provide a comma-separated list of\noptions for this question.",
       null=True)),
     migrations.AlterField(model_name='question',
       name='survey',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
       related_name='related_questions',
       to='survey.Survey')),
     migrations.AlterField(model_name='response',
       name='survey',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
       related_name='responses',
       to='survey.Survey'))]