# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-trello-webhooks/lib/python2.7/site-packages/trello_webhooks/migrations/0002_webhook_is_active.py
# Compiled at: 2014-12-03 14:27:17
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('trello_webhooks', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'webhook', name=b'is_active', field=models.NullBooleanField(default=None), preserve_default=True)]