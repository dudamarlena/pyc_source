# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_message/migrations/0001_initial.py
# Compiled at: 2018-10-18 03:10:10
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Message', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, verbose_name=b'消息名称')),
      (
       b'info', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'说明')),
      (
       b'is_user_show', models.BooleanField(default=False, verbose_name=b'学生页是否显示')),
      (
       b'is_admin_show', models.BooleanField(default=False, verbose_name=b'管理页是否显示')),
      (
       b'identity', models.CharField(help_text=b'此字段唯一', max_length=180, null=True, unique=True, verbose_name=b'标识符'))], options={b'ordering': [
                    b'id'], 
        b'db_table': b'bee_django_message'}),
     migrations.CreateModel(name=b'SendRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=180, verbose_name=b'主题')),
      (
       b'info', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'内容')),
      (
       b'is_view', models.BooleanField(default=False, verbose_name=b'是否看过')),
      (
       b'sent_at', models.DateTimeField(auto_now_add=True, verbose_name=b'发送时间')),
      (
       b'url', models.CharField(max_length=180, null=True, verbose_name=b'点击后跳转到的页面')),
      (
       b'from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_message_from_user', to=settings.AUTH_USER_MODEL, verbose_name=b'来自')),
      (
       b'message', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'record_message', to=b'bee_django_message.Message')),
      (
       b'to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_message_to_user', to=settings.AUTH_USER_MODEL, verbose_name=b'发送给'))], options={b'ordering': [
                    b'-sent_at'], 
        b'db_table': b'bee_django_message_record'})]