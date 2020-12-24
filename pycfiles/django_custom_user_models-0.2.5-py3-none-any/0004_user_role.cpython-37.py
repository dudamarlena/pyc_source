# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\migrations\0004_user_role.py
# Compiled at: 2019-12-11 08:47:03
# Size of source mod 2**32: 611 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('CustomAuth', '0003_role')]
    operations = [
     migrations.AddField(model_name='user',
       name='role',
       field=models.ForeignKey(blank=True, help_text='Specific role for this user', null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='users', related_query_name='user', to='CustomAuth.Role', verbose_name='user role'))]