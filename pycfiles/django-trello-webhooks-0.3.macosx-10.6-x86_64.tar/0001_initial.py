# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-trello-webhooks/lib/python2.7/site-packages/trello_webhooks/migrations/0001_initial.py
# Compiled at: 2014-12-03 14:27:17
from __future__ import unicode_literals
from django.db import models, migrations
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'CallbackEvent', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'timestamp', models.DateTimeField()),
      (
       b'event_type', models.CharField(max_length=50)),
      (
       b'event_payload', jsonfield.fields.JSONField(default=dict))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Webhook', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'trello_model_id', models.CharField(help_text=b'The id of the model being watched.', max_length=24)),
      (
       b'trello_id', models.CharField(help_text=b'Webhook id returned from Trello API.', max_length=24, blank=True)),
      (
       b'description', models.CharField(help_text=b'Description of the webhook.', max_length=500, blank=True)),
      (
       b'auth_token', models.CharField(help_text=b'The Trello API user auth token.', max_length=64)),
      (
       b'created_at', models.DateTimeField(blank=True)),
      (
       b'last_updated_at', models.DateTimeField(blank=True))], options={}, bases=(
      models.Model,)),
     migrations.AddField(model_name=b'callbackevent', name=b'webhook', field=models.ForeignKey(to=b'trello_webhooks.Webhook'), preserve_default=True)]