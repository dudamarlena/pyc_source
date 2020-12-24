# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_track/migrations/0001_initial.py
# Compiled at: 2018-08-10 05:46:33
from __future__ import unicode_literals
import bee_django_track.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'ContentType', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=180, verbose_name=b'标题')),
      (
       b'identity', models.CharField(help_text=b'此字段唯一', max_length=180, null=True, unique=True, verbose_name=b'标识符')),
      (
       b'app_label', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'app名')),
      (
       b'model', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'模块名')),
      (
       b'user_field', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'用户字段名')),
      (
       b'link', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'链接')),
      (
       b'link_type', models.IntegerField(default=1)),
      (
       b'info', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'备注')),
      (
       b'is_add', models.BooleanField(default=True, verbose_name=b'是否可添加')),
      (
       b'is_edit', models.BooleanField(default=True, verbose_name=b'是否可修改'))], options={b'ordering': [
                    b'id'], 
        b'db_table': b'bee_django_track_content_type'}),
     migrations.CreateModel(name=b'UserTrackRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=180, verbose_name=b'标题')),
      (
       b'info', models.TextField(verbose_name=b'详情')),
      (
       b'content_id', models.IntegerField(null=True, verbose_name=bee_django_track.models.ContentType)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_track.ContentType', verbose_name=b'类型')),
      (
       b'created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'create_by_user', to=settings.AUTH_USER_MODEL, verbose_name=b'由谁添加')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'用户'))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_track_record'}),
     migrations.AlterUniqueTogether(name=b'contenttype', unique_together=set([('app_label', 'model')]))]