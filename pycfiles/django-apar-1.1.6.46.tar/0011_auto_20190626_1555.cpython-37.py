# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/reviews/migrations/0011_auto_20190626_1555.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 747 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('reviews', '0010_auto_20190626_1549'),
     ('questionanswers', '0010_auto_20190626_1549')]
    operations = [
     migrations.RemoveField(model_name='basereview',
       name='user_obj'),
     migrations.AlterField(model_name='review',
       name='user_obj_2',
       field=models.ForeignKey(default=1, on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL), verbose_name='User'),
       preserve_default=False)]