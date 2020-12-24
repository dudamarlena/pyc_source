# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0001_initial.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'ContentType', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'app_label', models.CharField(max_length=180, verbose_name=b'app名')),
      (
       b'model', models.CharField(max_length=180, verbose_name=b'模块名')),
      (
       b'user_field', models.CharField(max_length=180, verbose_name=b'用户字段名')),
      (
       b'info', models.CharField(max_length=180, null=True, verbose_name=b'备注'))], options={b'ordering': [
                    b'id'], 
        b'db_table': b'bee_django_mission_content_type'}),
     migrations.CreateModel(name=b'Line', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, verbose_name=b'标题')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'line_type', models.IntegerField(choices=[(1, '长期任务'), (2, '周任务')], default=0)),
      (
       b'auto_finish', models.BooleanField(default=True, verbose_name=b'是否自动完成')),
      (
       b'auto_start', models.BooleanField(default=True, verbose_name=b'是否自动开启下一个'))], options={b'ordering': [
                    b'id'], 
        b'db_table': b'bee_django_mission_line', 
        b'verbose_name': b'任务线'}),
     migrations.CreateModel(name=b'Mission', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, verbose_name=b'标题')),
      (
       b'count', models.IntegerField(verbose_name=b'数量')),
      (
       b'info', models.TextField(blank=True, null=True, verbose_name=b'备注')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'order_by', models.IntegerField(blank=True, null=True, verbose_name=b'顺序'))], options={b'ordering': [
                    b'created_at'], 
        b'db_table': b'bee_django_mission', 
        b'verbose_name': b'任务'}),
     migrations.CreateModel(name=b'MissionType', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, unique=True, verbose_name=b'标题')),
      (
       b'aggregate_type', models.IntegerField(choices=[(1, 'Count'), (2, 'Sum'), (3, 'TruncDay')], default=1, verbose_name=b'聚合类型')),
      (
       b'field_name', models.CharField(default=b'id', max_length=180, verbose_name=b'取值字段名')),
      (
       b'timestamp_field', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'时间字段名')),
      (
       b'comparison_type', models.IntegerField(choices=[(1, '>='), (2, '>')], default=1, verbose_name=b'比较类型')),
      (
       b'operator_type', models.IntegerField(choices=[(0, '无'), (1, '* 60')], default=0, verbose_name=b'对值运算')),
      (
       b'conditions', models.TextField(blank=True, help_text=b'格式为：[条件1：值1，条件2：值2]，多个条件用,分割', null=True, verbose_name=b'其他附加条件')),
      (
       b'link_url', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'链接地址')),
      (
       b'link_name', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'链接名字')),
      (
       b'content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_mission.ContentType', verbose_name=b'app及model'))], options={b'ordering': [
                    b'id'], 
        b'db_table': b'bee_django_mission_type', 
        b'verbose_name': b'任务类型'}),
     migrations.CreateModel(name=b'Stage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'level', models.IntegerField(null=True, verbose_name=b'阶段')),
      (
       b'name', models.CharField(max_length=180, verbose_name=b'标题')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'line', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_mission.Line'))], options={b'ordering': [
                    b'level'], 
        b'db_table': b'bee_django_mission_stage', 
        b'verbose_name': b'阶段任务'}),
     migrations.CreateModel(name=b'UserLine', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'start_at', models.DateTimeField(auto_now_add=True)),
      (
       b'finish_at', models.DateTimeField(null=True)),
      (
       b'line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_mission.Line')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'start_at'], 
        b'db_table': b'bee_django_mission_user_line', 
        b'verbose_name': b'学生任务线'}),
     migrations.CreateModel(name=b'UserMission', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'custom_name', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'自定义名字')),
      (
       b'custom_count', models.IntegerField(blank=True, null=True, verbose_name=b'自定义数量')),
      (
       b'finish_at', models.DateTimeField(null=True)),
      (
       b'mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_mission.Mission'))], options={b'ordering': [
                    b'finish_at'], 
        b'db_table': b'bee_django_mission_user_mission', 
        b'verbose_name': b'学生的任务'}),
     migrations.CreateModel(name=b'UserStage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, null=True, verbose_name=b'标题')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'添加时间')),
      (
       b'start_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'开始时间')),
      (
       b'finish_at', models.DateTimeField(null=True, verbose_name=b'完成时间')),
      (
       b'end_at', models.DateTimeField(null=True, verbose_name=b'结束时间')),
      (
       b'stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_mission.Stage')),
      (
       b'user_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_mission.UserLine'))], options={b'ordering': [
                    b'start_at'], 
        b'db_table': b'bee_django_mission_user_stage', 
        b'verbose_name': b'学生阶段任务'}),
     migrations.AddField(model_name=b'usermission', name=b'user_stage', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_mission.UserStage')),
     migrations.AddField(model_name=b'mission', name=b'mission_type', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_mission.MissionType')),
     migrations.AddField(model_name=b'mission', name=b'stage', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_mission.Stage')),
     migrations.AlterUniqueTogether(name=b'contenttype', unique_together=set([('app_label', 'model')])),
     migrations.AlterUniqueTogether(name=b'stage', unique_together=set([('line', 'level')]))]