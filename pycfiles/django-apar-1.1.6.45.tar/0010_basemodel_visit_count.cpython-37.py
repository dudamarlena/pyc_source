# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0010_basemodel_visit_count.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 446 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0009_basemodel_sort')]
    operations = [
     migrations.AddField(model_name='basemodel',
       name='visit_count',
       field=models.IntegerField(default=0, verbose_name='Visit counter'))]