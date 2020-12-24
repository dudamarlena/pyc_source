# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0059_userquestionanswerrecord.py
# Compiled at: 2018-09-28 06:04:41
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_course', '0059_sectionattach_name')]
    operations = [
     migrations.CreateModel(name=b'UserQuestionAnswerRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.SectionQuestionOption')),
      (
       b'question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.SectionQuestion')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_course_user_question_answer_record'})]