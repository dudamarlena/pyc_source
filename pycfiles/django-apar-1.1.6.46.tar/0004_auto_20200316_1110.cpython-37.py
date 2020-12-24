# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/bookmarks/migrations/0004_auto_20200316_1110.py
# Compiled at: 2020-03-16 03:40:40
# Size of source mod 2**32: 1350 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bookmarks', '0003_auto_20190615_1430')]
    operations = [
     migrations.AlterModelOptions(name='bookmark',
       options={'verbose_name':'Bookmark', 
      'verbose_name_plural':'Bookmarks'}),
     migrations.AlterField(model_name='bookmark',
       name='created_at',
       field=models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
     migrations.AlterField(model_name='bookmark',
       name='model_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='bookmark_obj', to='basemodels.BaseModel', verbose_name='Model')),
     migrations.AlterField(model_name='bookmark',
       name='update_at',
       field=models.DateTimeField(auto_now=True, verbose_name='Update at')),
     migrations.AlterField(model_name='bookmark',
       name='user_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL), verbose_name='User'))]