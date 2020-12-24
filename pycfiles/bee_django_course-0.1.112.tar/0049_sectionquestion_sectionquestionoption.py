# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0049_sectionquestion_sectionquestionoption.py
# Compiled at: 2018-09-04 03:24:37
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0048_userlivecomment')]
    operations = [
     migrations.CreateModel(name=b'SectionQuestion', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'question', models.CharField(max_length=180, verbose_name=b'问题')),
      (
       b'question_type', models.IntegerField(choices=[(1, '单选'), (2, '多选')], default=1, verbose_name=b'问题类型')),
      (
       b'order_by', models.IntegerField(default=0, verbose_name=b'顺序')),
      (
       b'section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.Section', verbose_name=b'关联的课件'))], options={b'ordering': [
                    b'order_by'], 
        b'db_table': b'bee_django_course_section_question'}),
     migrations.CreateModel(name=b'SectionQuestionOption', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'option', models.CharField(max_length=180, verbose_name=b'选项')),
      (
       b'order_by', models.IntegerField(default=0, verbose_name=b'顺序')),
      (
       b'is_correct', models.BooleanField(default=False, verbose_name=b'是否正确答案')),
      (
       b'question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.SectionQuestion', verbose_name=b'问题'))], options={b'ordering': [
                    b'order_by'], 
        b'db_table': b'bee_django_course_section_question_option'})]