# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/pages/migrations/0003_page_is_show_in_home.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0002_page_english_title')]
    operations = [
     migrations.AddField(model_name=b'page', name=b'is_show_in_home', field=models.BooleanField(default=True, verbose_name=b'Is Show in home'))]