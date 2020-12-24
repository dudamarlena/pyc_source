# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/golm_admin/migrations/0002_chat.py
# Compiled at: 2018-04-15 16:14:23
# Size of source mod 2**32: 641 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('golm_admin', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Chat',
       fields=[
      (
       'chat_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
      (
       'user_uid', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='golm_admin.User'))])]