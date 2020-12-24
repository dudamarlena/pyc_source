# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/chats/migrations/0002_chatsession_type.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 526 bytes
import aparnik.contrib.chats.models
from django.db import migrations
import django_enumfield.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('chats', '0001_initial')]
    operations = [
     migrations.AddField(model_name='chatsession',
       name='type',
       field=django_enumfield.db.fields.EnumField(default=1, enum=(aparnik.contrib.chats.models.ChatSessionTypeEnum), verbose_name='Type'))]