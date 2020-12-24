# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/bookmarks/migrations/0003_auto_20190615_1430.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1436 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bookmarks', '0002_auto_20181026_1745')]
    operations = [
     migrations.AlterModelOptions(name='bookmark',
       options={'verbose_name':'بوکمارک', 
      'verbose_name_plural':'بوکمارک ها'}),
     migrations.AlterField(model_name='bookmark',
       name='created_at',
       field=models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')),
     migrations.AlterField(model_name='bookmark',
       name='model_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='bookmark_obj', to='basemodels.BaseModel', verbose_name='چه چیز را نمایش دهد؟')),
     migrations.AlterField(model_name='bookmark',
       name='update_at',
       field=models.DateTimeField(auto_now=True, verbose_name='بروزرسانی شده در')),
     migrations.AlterField(model_name='bookmark',
       name='user_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL), verbose_name='کاربر'))]