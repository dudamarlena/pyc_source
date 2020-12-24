# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0004_auto_20181103_2233.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 557 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0003_basemodel_update_needed')]
    operations = [
     migrations.AlterField(model_name='basemodel',
       name='update_needed',
       field=models.BooleanField(default=False, verbose_name='\\u0646\\u06cc\\u0627\\u0632 \\u0628\\u0647 \\u0628\\u0631\\u0648\\u0632\\u0631\\u0633\\u0627\\u0646\\u06cc'))]