# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_auth_valimo/migrations/0001_initial.py
# Compiled at: 2016-09-19 07:37:17
from __future__ import unicode_literals
from django.db import migrations, models
import nodeconductor_auth_valimo.models, django.utils.timezone
from django.conf import settings
import django_fsm, nodeconductor.core.fields, model_utils.fields

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'AuthResult', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'error_message', models.TextField(blank=True)),
      (
       b'phone', models.CharField(max_length=30)),
      (
       b'message', models.CharField(default=nodeconductor_auth_valimo.models._default_message, help_text=b'This message will be shown to user.', max_length=4)),
      (
       b'state', django_fsm.FSMField(default=b'Scheduled', max_length=50, choices=[('Scheduled', 'Scheduled'), ('Processing', 'Processing'), ('OK', 'OK'), ('Canceled', 'Canceled'), ('Erred', 'Erred')])),
      (
       b'details', models.CharField(help_text=b'Cancellation details.', max_length=255, blank=True)),
      (
       b'backend_transaction_id', models.CharField(max_length=100, blank=True)),
      (
       b'user', models.ForeignKey(related_name=b'auth_valimo_results', to=settings.AUTH_USER_MODEL, null=True))], options={b'abstract': False})]