# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\migrations\0003_role.py
# Compiled at: 2019-12-11 08:46:54
# Size of source mod 2**32: 973 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('auth', '0011_update_proxy_permissions'),
     ('CustomAuth', '0002_date_joined_auto_now_add')]
    operations = [
     migrations.CreateModel(name='Role',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=250, verbose_name='name of role')),
      (
       'permissions', models.ManyToManyField(blank=True, null=True, related_name='roles', related_query_name='role', to='auth.Permission', verbose_name='Role Permission'))],
       options={'verbose_name':'role', 
      'verbose_name_plural':'roles', 
      'ordering':('name', )})]