# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0038_userlevel_userleveluprecord.py
# Compiled at: 2019-10-16 02:51:30
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('auth', '0008_alter_user_username_max_length'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_user', '0037_auto_20191012_1354')]
    operations = [
     migrations.CreateModel(name=b'UserLevel', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=180, verbose_name=b'标题')),
      (
       b'level', models.IntegerField(default=0, verbose_name=b'级别')),
      (
       b'detail', models.TextField(blank=True, null=True, verbose_name=b'详情')),
      (
       b'after_group', models.ManyToManyField(help_text=b'（不可多选）', related_name=b'user_after_group', to=b'auth.Group', verbose_name=b'升级后的用户组')),
      (
       b'before_group', models.ManyToManyField(help_text=b'（可多选）', related_name=b'user_before_group', to=b'auth.Group', verbose_name=b'可升级用户组'))], options={b'ordering': [
                    b'level'], 
        b'db_table': b'bee_django_user_level', 
        b'permissions': (('view_level_list', '可以查看用户升级列表'), )}),
     migrations.CreateModel(name=b'UserLevelUpRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'updated_at', models.DateTimeField(auto_now=True)),
      (
       b'status', models.IntegerField(blank=True, choices=[(-1, '未申请'), (-2, '已申请'), (1, '通过'), (2, '未通过'), (3, '关闭')], default=-1, null=True, verbose_name=b'状态')),
      (
       b'detail', models.TextField(blank=True, null=True, verbose_name=b'详情')),
      (
       b'info', models.TextField(blank=True, null=True, verbose_name=b'其他')),
      (
       b'level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=b'bee_django_user_level', to=b'bee_django_user.UserLevel', verbose_name=b'级别')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_django_level_up_user', to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_user_level_up_record'})]