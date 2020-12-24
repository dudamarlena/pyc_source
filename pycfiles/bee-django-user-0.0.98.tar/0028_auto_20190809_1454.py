# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0028_auto_20190809_1454.py
# Compiled at: 2019-08-09 02:54:34
from __future__ import unicode_literals
from django.db import migrations
import imagekit.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0027_auto_20190807_1410')]
    operations = [
     migrations.AlterField(model_name=b'userprofile', name=b'avatar', field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=b'avatars', verbose_name=b'头像'))]