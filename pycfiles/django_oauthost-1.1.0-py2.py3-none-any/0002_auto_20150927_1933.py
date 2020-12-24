# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shared/idle/code/i/django-env/apps/oauthost/migrations/0002_auto_20150927_1933.py
# Compiled at: 2015-09-27 13:33:57
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('oauthost', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'authorizationcode', name=b'code', field=models.CharField(verbose_name=b'Code', blank=True, max_length=7, help_text=b'Code issued upon authorization.', unique=True)),
     migrations.AlterField(model_name=b'authorizationcode', name=b'scopes', field=models.ManyToManyField(verbose_name=b'Scopes', blank=True, help_text=b'The scopes token issued with this code should be restricted to.', to=b'oauthost.Scope')),
     migrations.AlterField(model_name=b'client', name=b'scopes', field=models.ManyToManyField(verbose_name=b'Scopes', blank=True, help_text=b'The scopes client is restricted to. <i>All registered scopes will be available for the client if none selected.</i>', to=b'oauthost.Scope')),
     migrations.AlterField(model_name=b'token', name=b'access_token', field=models.CharField(verbose_name=b'Access Token', blank=True, max_length=32, help_text=b'Token to be used to access resources.', unique=True)),
     migrations.AlterField(model_name=b'token', name=b'access_token_type', field=models.CharField(choices=[('bearer', 'Bearer')], verbose_name=b'Type', max_length=100, help_text=b'Access token type client uses to apply the appropriate authorization method.', default=b'bearer')),
     migrations.AlterField(model_name=b'token', name=b'scopes', field=models.ManyToManyField(verbose_name=b'Scopes', blank=True, help_text=b'The scopes token is restricted to.', to=b'oauthost.Scope'))]