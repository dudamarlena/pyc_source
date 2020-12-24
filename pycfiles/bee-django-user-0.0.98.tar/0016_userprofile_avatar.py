# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0016_userprofile_avatar.py
# Compiled at: 2019-03-13 07:53:36
from __future__ import unicode_literals
from django.db import migrations
import imagekit.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0015_auto_20181219_2057')]
    operations = [
     migrations.AddField(model_name=b'userprofile', name=b'avatar', field=imagekit.models.fields.ProcessedImageField(blank=True, default=b'avatars/default.jpg', null=True, upload_to=b'avatars', verbose_name=b'头像'))]