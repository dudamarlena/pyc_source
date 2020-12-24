# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/pages/migrations/0002_page_english_title.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'page', name=b'english_title', field=models.CharField(default=b'home', max_length=100, verbose_name=b'English Title'), preserve_default=False)]