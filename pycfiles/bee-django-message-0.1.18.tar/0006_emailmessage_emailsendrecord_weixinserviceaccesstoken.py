# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_message/migrations/0006_emailmessage_emailsendrecord_weixinserviceaccesstoken.py
# Compiled at: 2019-08-12 06:20:42
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_message', '0005_auto_20181206_1951')]
    operations = [
     migrations.CreateModel(name=b'EmailMessage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, verbose_name=b'消息名称')),
      (
       b'to_user', models.CharField(max_length=180)),
      (
       b'info', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'说明')),
      (
       b'identity', models.CharField(help_text=b'此字段唯一', max_length=180, unique=True, verbose_name=b'标识符'))], options={b'ordering': [
                    b'id'], 
        b'db_table': b'bee_django_message_email'}),
     migrations.CreateModel(name=b'EmailSendRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=180, null=True)),
      (
       b'content', models.TextField(null=True)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'email_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'email_message', to=b'bee_django_message.EmailMessage')),
      (
       b'user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'email_send_record_user', to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_message_email_record'}),
     migrations.CreateModel(name=b'WeixinServiceAccessToken', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'token', models.CharField(max_length=180)),
      (
       b'appid', models.CharField(max_length=180)),
      (
       b'appsecrect', models.CharField(max_length=180)),
      (
       b'alias', models.CharField(max_length=180)),
      (
       b'expires', models.IntegerField()),
      (
       b'gettime', models.DateTimeField(auto_now_add=True))], options={b'db_table': b'bee_django_message_weixin_service_access_token'})]