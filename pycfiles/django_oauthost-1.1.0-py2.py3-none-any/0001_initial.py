# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: oauthost/../oauthost/migrations/0001_initial.py
# Compiled at: 2017-12-09 23:12:36
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings
import oauthost.fields

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'AuthorizationCode', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'date_issued', models.DateTimeField(auto_now_add=True, verbose_name=b'Issued at')),
      (
       b'code', models.CharField(help_text=b'Code issued upon authorization.', unique=True, max_length=7, verbose_name=b'Code')),
      (
       b'uri', oauthost.fields.URLSchemeField(help_text=b'The URI authorization is bound to.', verbose_name=b'Redirect URI'))], options={b'verbose_name': b'Authorization code', 
        b'verbose_name_plural': b'Authorization codes'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Client', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'date_registered', models.DateTimeField(auto_now_add=True, verbose_name=b'Registered at')),
      (
       b'title', models.CharField(unique=True, max_length=100, verbose_name=b'Title')),
      (
       b'description', models.TextField(max_length=100, verbose_name=b'Description')),
      (
       b'link', models.URLField(help_text=b'Application webpage URL.', null=True, verbose_name=b'URL', blank=True)),
      (
       b'identifier', models.CharField(help_text=b'Public client identifier. <i>Generated automatically if empty.</i>.', unique=True, max_length=250, verbose_name=b'Identifier', blank=True)),
      (
       b'token_lifetime', models.IntegerField(help_text=b'Time in seconds after which token given to the application expires.', null=True, verbose_name=b'Token lifetime', blank=True)),
      (
       b'password', models.CharField(help_text=b'Secret that can be used along with an identifier as username to authenticate with HTTP Basic scheme.', max_length=250, verbose_name=b'Password', blank=True)),
      (
       b'type', models.IntegerField(default=1, help_text=b'<b>Confidential</b> &#8212; Clients capable of maintaining the confidentiality of their credentials, or capable of secure client authentication using other means.<br /> <b>Public</b> &#8212; Clients incapable of maintaining the confidentiality of their credentials, and incapable of secure client authentication via any other means', verbose_name=b'Type', choices=[(1, 'Confidential'), (2, 'Public')])),
      (
       b'hash_sign_supported', models.BooleanField(default=True, help_text=b'Should be checked if this client supports fragment component (#) in the HTTP "Location" response header field', verbose_name=b'Supports # in "Location"'))], options={b'verbose_name': b'Client', 
        b'verbose_name_plural': b'Clients'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'RedirectionEndpoint', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'uri', oauthost.fields.URLSchemeField(help_text=b'URI or URI scheme for authorization server to redirect client when an interaction with a resource owner is complete.', verbose_name=b'URI')),
      (
       b'client', models.ForeignKey(related_name=b'redirection_uris', verbose_name=b'Client', to=b'oauthost.Client', on_delete=models.CASCADE))], options={b'verbose_name': b'Redirection Endpoint', 
        b'verbose_name_plural': b'Redirection Endpoints'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Scope', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'identifier', models.CharField(help_text=b'Scope identifier. Usually in form of `app_name:view_name`.', unique=True, max_length=100, verbose_name=b'Scope ID')),
      (
       b'title', models.CharField(help_text=b'Scope human-friendly name.', max_length=250, verbose_name=b'Scope title')),
      (
       b'status', models.PositiveIntegerField(default=1, db_index=True, verbose_name=b'Status', choices=[(1, 'Enabled'), (2, 'Disabled')]))], options={b'ordering': [
                    b'title'], 
        b'verbose_name': b'Scope', 
        b'verbose_name_plural': b'Scopes'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Token', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'date_issued', models.DateTimeField(auto_now_add=True, verbose_name=b'Issued at')),
      (
       b'expires_at', models.DateTimeField(null=True, verbose_name=b'Expires at', blank=True)),
      (
       b'access_token', models.CharField(help_text=b'Token to be used to access resources.', unique=True, max_length=32, verbose_name=b'Access Token')),
      (
       b'refresh_token', models.CharField(null=True, max_length=32, blank=True, help_text=b'Token to be used to refresh access token.', unique=True, verbose_name=b'Refresh Token')),
      (
       b'access_token_type', models.CharField(default=b'bearer', help_text=b'Access token type client uses to apply the appropriate authorization method.', max_length=100, verbose_name=b'Type', choices=[('bearer', 'Bearer')])),
      (
       b'client', models.ForeignKey(verbose_name=b'Client', to=b'oauthost.Client', help_text=b'The client application token is issued for.', on_delete=models.CASCADE)),
      (
       b'code', models.ForeignKey(blank=True, to=b'oauthost.AuthorizationCode', help_text=b'Authorization code used to generate this token.', null=True, verbose_name=b'Code', on_delete=models.CASCADE)),
      (
       b'scopes', models.ManyToManyField(help_text=b'The scopes token is restricted to.', to=b'oauthost.Scope', null=True, verbose_name=b'Scopes', blank=True)),
      (
       b'user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text=b'The user token is issued for.', null=True, verbose_name=b'User', on_delete=models.CASCADE))], options={b'verbose_name': b'Token', 
        b'verbose_name_plural': b'Tokens'}, bases=(
      models.Model,)),
     migrations.AddField(model_name=b'client', name=b'scopes', field=models.ManyToManyField(help_text=b'The scopes client is restricted to. <i>All registered scopes will be available for the client if none selected.</i>', to=b'oauthost.Scope', null=True, verbose_name=b'Scopes', blank=True), preserve_default=True),
     migrations.AddField(model_name=b'client', name=b'user', field=models.ForeignKey(verbose_name=b'Registrant', to=settings.AUTH_USER_MODEL, help_text=b'User who registered this client.', on_delete=models.CASCADE), preserve_default=True),
     migrations.AddField(model_name=b'authorizationcode', name=b'client', field=models.ForeignKey(verbose_name=b'Client', to=b'oauthost.Client', help_text=b'The client authorization is granted for.', on_delete=models.CASCADE), preserve_default=True),
     migrations.AddField(model_name=b'authorizationcode', name=b'scopes', field=models.ManyToManyField(help_text=b'The scopes token issued with this code should be restricted to.', to=b'oauthost.Scope', null=True, verbose_name=b'Scopes', blank=True), preserve_default=True),
     migrations.AddField(model_name=b'authorizationcode', name=b'user', field=models.ForeignKey(verbose_name=b'User', to=settings.AUTH_USER_MODEL, help_text=b'The user authorization is granted for.', on_delete=models.CASCADE), preserve_default=True)]