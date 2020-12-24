# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/golm_admin/migrations/0003_auto_20180207_2331.py
# Compiled at: 2018-04-15 16:14:23
# Size of source mod 2**32: 1539 bytes
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('golm_admin', '0002_chat')]
    operations = [
     migrations.CreateModel(name='Message',
       fields=[
      (
       'id', models.BigAutoField(primary_key=True, serialize=False)),
      (
       'text', models.TextField(blank=True, null=True)),
      (
       'is_from_user', models.BooleanField()),
      (
       'time', models.DateTimeField(auto_now=True)),
      (
       'intent', models.TextField(blank=True, db_index=True, max_length=255, null=True)),
      (
       'state', models.TextField(blank=True, db_index=True, max_length=255, null=True))]),
     migrations.CreateModel(name='QuickReply',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'text', models.TextField(max_length=255)),
      (
       'message', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='golm_admin.Message'))]),
     migrations.RemoveField(model_name='user',
       name='last_active'),
     migrations.AddField(model_name='message',
       name='chat',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='golm_admin.Chat'))]