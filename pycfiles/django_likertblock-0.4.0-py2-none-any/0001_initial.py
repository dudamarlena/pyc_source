# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/work/python/django-likertblock/likertblock/migrations/0001_initial.py
# Compiled at: 2016-05-03 06:31:35
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Question', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'text', models.TextField(blank=True))]),
     migrations.CreateModel(name=b'Questionnaire', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'description', models.TextField(blank=True))]),
     migrations.CreateModel(name=b'Response', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'value', models.IntegerField(default=0)),
      (
       b'question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'likertblock.Question'))]),
     migrations.CreateModel(name=b'Submission', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'submitted', models.DateTimeField(auto_now_add=True)),
      (
       b'questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'likertblock.Questionnaire')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'likert_submission', to=settings.AUTH_USER_MODEL))]),
     migrations.AddField(model_name=b'response', name=b'submission', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'likertblock.Submission')),
     migrations.AddField(model_name=b'question', name=b'questionnaire', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'likertblock.Questionnaire')),
     migrations.AlterOrderWithRespectTo(name=b'question', order_with_respect_to=b'questionnaire')]