# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/pages/migrations/0002_page_english_title.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 485 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0001_initial')]
    operations = [
     migrations.AddField(model_name='page',
       name='english_title',
       field=models.CharField(default='home', max_length=100, verbose_name='English Title'),
       preserve_default=False)]