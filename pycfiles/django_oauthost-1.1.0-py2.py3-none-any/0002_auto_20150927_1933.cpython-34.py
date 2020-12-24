# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shared/idle/code/i/blockada/web/venv/lib/python3.4/site-packages/oauthost/migrations/0002_auto_20150927_1933.py
# Compiled at: 2015-09-27 13:33:57
# Size of source mod 2**32: 1943 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('oauthost', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='authorizationcode', name='code', field=models.CharField(verbose_name='Code', blank=True, max_length=7, help_text='Code issued upon authorization.', unique=True)),
     migrations.AlterField(model_name='authorizationcode', name='scopes', field=models.ManyToManyField(verbose_name='Scopes', blank=True, help_text='The scopes token issued with this code should be restricted to.', to='oauthost.Scope')),
     migrations.AlterField(model_name='client', name='scopes', field=models.ManyToManyField(verbose_name='Scopes', blank=True, help_text='The scopes client is restricted to. <i>All registered scopes will be available for the client if none selected.</i>', to='oauthost.Scope')),
     migrations.AlterField(model_name='token', name='access_token', field=models.CharField(verbose_name='Access Token', blank=True, max_length=32, help_text='Token to be used to access resources.', unique=True)),
     migrations.AlterField(model_name='token', name='access_token_type', field=models.CharField(choices=[('bearer', 'Bearer')], verbose_name='Type', max_length=100, help_text='Access token type client uses to apply the appropriate authorization method.', default='bearer')),
     migrations.AlterField(model_name='token', name='scopes', field=models.ManyToManyField(verbose_name='Scopes', blank=True, help_text='The scopes token is restricted to.', to='oauthost.Scope'))]