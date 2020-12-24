# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/chats/migrations/0004_chatmessagenotification.py
# Compiled at: 2020-03-03 06:09:02
# Size of source mod 2**32: 1188 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('chats', '0003_auto_20200210_1451')]
    operations = [
     migrations.CreateModel(name='ChatMessageNotification',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'update_at', models.DateTimeField(auto_now=True)),
      (
       'is_read', models.BooleanField(default=False, verbose_name='Is read')),
      (
       'chat_message', models.ForeignKey(on_delete=(django.db.models.deletion.PROTECT), related_name='message_notifications', to='chats.ChatSessionMessage')),
      (
       'user', models.ForeignKey(on_delete=(django.db.models.deletion.PROTECT), to=(settings.AUTH_USER_MODEL)))],
       options={'abstract': False})]