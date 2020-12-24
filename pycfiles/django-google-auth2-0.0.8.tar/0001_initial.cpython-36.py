# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/GoogleAuthenticatorPyPI/django_google_auth/migrations/0001_initial.py
# Compiled at: 2019-04-01 22:15:42
# Size of source mod 2**32: 721 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='DjangoGoogleAuthenticator2',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'username', models.CharField(max_length=255, verbose_name='用户名')),
      (
       'key', models.CharField(max_length=255, unique=True, verbose_name='秘钥'))],
       options={'db_table': 'google_authenticator2'})]