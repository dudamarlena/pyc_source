# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/migrations/0004_polymorphic_answers_to_kiss.py
# Compiled at: 2020-01-26 10:04:57
# Size of source mod 2**32: 1283 bytes
from django.db import migrations, models

def migrate_answers(apps, schema_editor):
    classes = []
    classes_str = [
     'AnswerText', 'AnswerInteger', 'AnswerRadio', 'AnswerSelect', 'AnswerSelectMultiple']
    for class_name in classes_str:
        classes.append(apps.get_model('survey', class_name))

    for class_ in classes:
        for answer in class_.objects.all():
            answer.new_body = answer.body
            answer.save()


class Migration(migrations.Migration):
    dependencies = [
     ('survey', '0003_auto_20170320_0337')]
    operations = [
     migrations.AddField(model_name='answerbase', name='new_body', field=models.TextField(blank=True, null=True)),
     migrations.RunPython(migrate_answers),
     migrations.DeleteModel(name='AnswerInteger'),
     migrations.DeleteModel(name='AnswerRadio'),
     migrations.DeleteModel(name='AnswerSelect'),
     migrations.DeleteModel(name='AnswerSelectMultiple'),
     migrations.DeleteModel(name='AnswerText'),
     migrations.RenameField('AnswerBase', 'new_body', 'body'),
     migrations.RenameModel('AnswerBase', 'Answer')]