# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/questionanswers/migrations/0006_auto_20190613_1829.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 776 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('questionanswers', '0005_auto_20190613_1815'),
     ('reviews', '0006_auto_20190613_1815')]
    operations = [
     migrations.AlterField(model_name='qa',
       name='model_obj2',
       field=models.ForeignKey(default=1, on_delete=(django.db.models.deletion.CASCADE), related_name='question_answers_set', to='basemodels.BaseModel', verbose_name='\\u0686\\u0647 \\u0686\\u06cc\\u0632 \\u0631\\u0627 \\u0646\\u0645\\u0627\\u06cc\\u0634 \\u062f\\u0647\\u062f\\u061f'),
       preserve_default=False)]