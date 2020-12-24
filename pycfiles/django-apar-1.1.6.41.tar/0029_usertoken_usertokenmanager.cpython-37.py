# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0029_usertoken_usertokenmanager.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1493 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0028_auto_20190615_1430')]
    operations = [
     migrations.CreateModel(name='UserTokenManager',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'))]),
     migrations.CreateModel(name='UserToken',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'token', models.CharField(max_length=500, verbose_name='Token')),
      (
       'is_active', models.BooleanField(default=True, verbose_name='Is active')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'update_at', models.DateTimeField(auto_now=True)),
      (
       'device_obj', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='aparnik_users.DeviceLogin', verbose_name='Device')),
      (
       'user_obj', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='token_user', to=(settings.AUTH_USER_MODEL), verbose_name='User'))],
       options={'unique_together': {('token', 'user_obj')}})]