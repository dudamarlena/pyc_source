# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0050_sectionquestion_options.py
# Compiled at: 2018-09-06 03:38:42
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0049_sectionquestion_sectionquestionoption')]
    operations = [
     migrations.AddField(model_name=b'sectionquestion', name=b'options', field=models.ManyToManyField(to=b'bee_django_course.SectionQuestionOption'))]