# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-jwt/lib/python2.7/site-packages/django_jwt/migrations/0001_initial.py
# Compiled at: 2015-12-28 11:05:50
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'RequestToken', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'target_url', models.CharField(help_text=b'The target endpoint.', max_length=200)),
      (
       b'expiration_time', models.DateTimeField(help_text=b'DateTime at which this token expires.', null=True, blank=True)),
      (
       b'not_before_time', models.DateTimeField(help_text=b'DateTime before which this token is invalid.', null=True, blank=True)),
      (
       b'data', models.TextField(help_text=b'Custom data (JSON) added to the default payload.', max_length=1000, blank=True)),
      (
       b'issued_at', models.DateTimeField(help_text=b'Time the token was created, set in the initial save.', null=True, blank=True)),
      (
       b'max_uses', models.IntegerField(default=1, help_text=b'Cap on the number of times the token can be used, defaults to 1 (single use).')),
      (
       b'used_to_date', models.IntegerField(default=0, help_text=b'Denormalised count of the number times the token has been used.')),
      (
       b'user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text=b'Intended recipient of the JWT.', null=True))]),
     migrations.CreateModel(name=b'RequestTokenLog', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'user_agent', models.TextField(help_text=b'User-agent of client used to make the request.', blank=True)),
      (
       b'client_ip', models.CharField(help_text=b'Client IP of device used to make the request.', max_length=15)),
      (
       b'timestamp', models.DateTimeField(help_text=b'Time the request was logged.')),
      (
       b'token', models.ForeignKey(help_text=b'The RequestToken that was used.', to=b'django_jwt.RequestToken')),
      (
       b'user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text=b'The user who made the request (None if anonymous).', null=True))])]