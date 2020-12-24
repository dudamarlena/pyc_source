# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/questionanswers/migrations/0013_auto_20200316_1110.py
# Compiled at: 2020-03-16 03:40:40
# Size of source mod 2**32: 1179 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('questionanswers', '0012_auto_20190626_1555')]
    operations = [
     migrations.AlterModelOptions(name='qa',
       options={'verbose_name':'Question Answer', 
      'verbose_name_plural':'Questions Answers'}),
     migrations.AlterField(model_name='qa',
       name='files',
       field=models.ManyToManyField(blank=True, to='filefields.FileField', verbose_name='Files')),
     migrations.AlterField(model_name='qa',
       name='model_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='question_answers_set', to='basemodels.BaseModel', verbose_name='Model')),
     migrations.AlterField(model_name='qa',
       name='user_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL), verbose_name='User'))]