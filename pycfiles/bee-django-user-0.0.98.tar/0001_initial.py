# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0001_initial.py
# Compiled at: 2018-06-14 06:29:05
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_crm', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'UserClass', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, verbose_name=b'班级名称')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'assistant',
       models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'助教'))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_user_class'}),
     migrations.CreateModel(name=b'UserProfile', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'student_id', models.IntegerField(null=True, unique=True, verbose_name=b'学号')),
      (
       b'room_id',
       models.CharField(blank=True, max_length=180, null=True, verbose_name=b'习琴室ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'preuser',
       models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.CRM_PREUSER, verbose_name=b'crm用户')),
      (
       b'user',
       models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
      (
       b'user_class',
       models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_user.UserClass', verbose_name=b'用户班级'))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_user_profile', 
        b'permissions': (
                       ('user.can_manage', 'can manage'), ('user.can_change', 'can change user info'),
                       ('user.can_change_group', 'can change user group'),
                       ('user.can_delete', 'can delete user'), ('user.can_create', 'can create user'),
                       ('user.view_all', 'view all users'), ('user.view_manage', 'view manage users'),
                       ('user.view_teach', 'view teach users'))})]