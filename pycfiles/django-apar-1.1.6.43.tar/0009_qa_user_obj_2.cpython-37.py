# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/questionanswers/migrations/0009_qa_user_obj_2.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 633 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('questionanswers', '0008_auto_20190615_1430')]
    operations = [
     migrations.AddField(model_name='qa',
       name='user_obj_2',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL), verbose_name='کاربر'))]