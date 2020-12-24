# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/work/python/django-quizblock-random/quizblock_random/migrations/0001_initial.py
# Compiled at: 2015-08-05 06:26:22
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     ('quizblock', '__first__'),
     ('pagetree', '0001_initial'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'QuestionUserLock', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'question_used', models.NullBooleanField()),
      (
       b'question_current', models.NullBooleanField()),
      (
       b'question', models.ForeignKey(to=b'quizblock.Question'))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'QuizRandom', fields=[
      (
       b'quiz_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'quizblock.Quiz')),
      (
       b'quiz_name', models.CharField(max_length=50)),
      (
       b'quiz_type', models.TextField(blank=True))], options={}, bases=('quizblock.quiz', )),
     migrations.AddField(model_name=b'questionuserlock', name=b'quiz', field=models.ForeignKey(to=b'quizblock_random.QuizRandom'), preserve_default=True),
     migrations.AddField(model_name=b'questionuserlock', name=b'section', field=models.ForeignKey(to=b'pagetree.Section'), preserve_default=True),
     migrations.AddField(model_name=b'questionuserlock', name=b'user', field=models.ForeignKey(to=settings.AUTH_USER_MODEL), preserve_default=True)]