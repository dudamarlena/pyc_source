# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/questionanswers/migrations/0003_auto_20181120_1055.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 505 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('questionanswers', '0002_auto_20181026_1745')]
    operations = [
     migrations.AlterField(model_name='qa',
       name='files',
       field=models.ManyToManyField(blank=True, to='filefields.FileField', verbose_name='\\u0641\\u0627\\u06cc\\u0644 \\u0647\\u0627'))]