# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/chats/migrations/0003_auto_20200210_1451.py
# Compiled at: 2020-03-03 06:09:02
# Size of source mod 2**32: 1301 bytes
import aparnik.contrib.chats.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0013_auto_20190714_1639'),
     ('chats', '0002_chatsession_type')]
    operations = [
     migrations.AddField(model_name='chatsession',
       name='cover_obj',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.PROTECT), to='filefields.FileField', verbose_name='Cover')),
     migrations.AddField(model_name='chatsession',
       name='title',
       field=models.CharField(blank=True, default='', max_length=255, verbose_name='Title')),
     migrations.AlterField(model_name='chatsession',
       name='owner',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.PROTECT), to=(settings.AUTH_USER_MODEL), verbose_name='Owner')),
     migrations.AlterField(model_name='chatsession',
       name='uri',
       field=models.URLField(default=(aparnik.contrib.chats.models._generate_unique_uri), verbose_name='Uri'))]