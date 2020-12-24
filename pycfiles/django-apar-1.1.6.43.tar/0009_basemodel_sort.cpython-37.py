# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0009_basemodel_sort.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 487 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0008_auto_20181211_1552')]
    operations = [
     migrations.AddField(model_name='basemodel',
       name='sort',
       field=models.IntegerField(default=0, verbose_name='\\u0645\\u0631\\u062a\\u0628 \\u0633\\u0627\\u0632\\u06cc'))]