# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-jwt/lib/python2.7/site-packages/django_jwt/migrations/0002_auto_20151227_1428.py
# Compiled at: 2015-12-28 11:05:50
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('django_jwt', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'requesttokenlog', name=b'status_code', field=models.IntegerField(help_text=b'Response status code associated with this use of the token.', null=True, blank=True)),
     migrations.AlterField(model_name=b'requesttoken', name=b'data', field=models.TextField(default=b'{}', help_text=b'Custom data (JSON) added to the default payload.', max_length=1000, blank=True)),
     migrations.AlterField(model_name=b'requesttokenlog', name=b'timestamp', field=models.DateTimeField(help_text=b'Time the request was logged.', blank=True))]