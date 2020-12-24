# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0007_auto_20190418_1409.py
# Compiled at: 2019-04-18 02:09:52
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_course_simple', '0006_auto_20190418_1318')]
    operations = [
     migrations.CreateModel(name=b'UserCourse', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'status', models.IntegerField(default=0, verbose_name=b'状态')),
      (
       b'passed_at', models.DateTimeField(blank=True, null=True)),
      (
       b'course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Course', verbose_name=b'课程')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'simple_course_user', to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_course_simple_user_course'}),
     migrations.CreateModel(name=b'UserPart', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'passed_at', models.DateTimeField(blank=True, null=True)),
      (
       b'status', models.IntegerField(default=0)),
      (
       b'part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Part'))], options={b'ordering': [
                    b'part__number'], 
        b'db_table': b'bee_django_course_simple_user_part'}),
     migrations.CreateModel(name=b'UserQuestion', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'passed_at', models.DateTimeField(auto_now_add=True)),
      (
       b'answer_option_id', models.IntegerField(null=True)),
      (
       b'question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Question')),
      (
       b'user_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.UserPart'))], options={b'ordering': [
                    b'question__number'], 
        b'db_table': b'bee_django_course_simple_user_question'}),
     migrations.CreateModel(name=b'UserSection', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'passed_at', models.DateTimeField(blank=True, null=True)),
      (
       b'status', models.IntegerField(default=0)),
      (
       b'section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Section')),
      (
       b'user_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.UserCourse'))], options={b'ordering': [
                    b'section__number'], 
        b'db_table': b'bee_django_course_simple_user_section'}),
     migrations.CreateModel(name=b'UserVideo', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'passed_at', models.DateTimeField(auto_now_add=True)),
      (
       b'user_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.UserPart')),
      (
       b'video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Video'))], options={b'ordering': [
                    b'video__number'], 
        b'db_table': b'bee_django_course_simple_user_video'}),
     migrations.AddField(model_name=b'userpart', name=b'user_section', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.UserSection'))]