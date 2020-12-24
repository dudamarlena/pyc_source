# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0006_user_avatar.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 654 bytes
from django.db import migrations, models
import django.db.models.deletion, django.core.validators
from aparnik.utils import fields

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0001_initial'),
     ('aparnik_users', '0005_auto_20181025_1601')]
    operations = [
     migrations.AddField(model_name='user',
       name='avatar',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='filefields.FileField', verbose_name='Avatar'))]