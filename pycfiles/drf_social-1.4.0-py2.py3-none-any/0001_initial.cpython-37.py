# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramzi/drf-social-auth/drf_social/migrations/0001_initial.py
# Compiled at: 2020-03-05 04:26:47
# Size of source mod 2**32: 947 bytes
from django.db import migrations, models
import drf_social.models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='AuthProvider',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=20)),
      (
       'provider', models.CharField(choices=[(drf_social.models.Providers('FACEBOOK'), drf_social.models.Providers('FACEBOOK')), (drf_social.models.Providers('GOOGLE'), drf_social.models.Providers('GOOGLE'))], max_length=10)),
      (
       'client_id', models.CharField(max_length=100)),
      (
       'client_secret', models.CharField(max_length=100)),
      (
       'scopes', models.TextField(default='[]'))])]