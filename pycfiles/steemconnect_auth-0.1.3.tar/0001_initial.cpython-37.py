# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ABRA\AppData\Local\Temp\pip-install-9f4wujyx\steemconnect-auth\steemconnect_auth\migrations\0001_initial.py
# Compiled at: 2019-05-20 22:11:00
# Size of source mod 2**32: 1104 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='SteemConnectUser',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'refresh_token', models.CharField(help_text='steemconnect user code / to get get_refresh_token', max_length=500)),
      (
       'code', models.CharField(help_text='steemconnect user code / to get get_refresh_token', max_length=500)),
      (
       'access_token', models.CharField(help_text='steemconnect user access_token to any operations', max_length=500)),
      (
       'user', models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))])]