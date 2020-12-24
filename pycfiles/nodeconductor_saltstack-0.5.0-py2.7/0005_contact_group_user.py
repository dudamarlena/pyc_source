# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/migrations/0005_contact_group_user.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations
import nodeconductor.core.fields, nodeconductor.core.validators

class Migration(migrations.Migration):
    dependencies = [
     ('exchange', '0004_init_quotas')]
    operations = [
     migrations.CreateModel(name=b'Contact', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'backend_id', models.CharField(db_index=True, max_length=255)),
      (
       b'email', models.EmailField(max_length=255)),
      (
       b'first_name', models.CharField(max_length=255)),
      (
       b'last_name', models.CharField(max_length=255)),
      (
       b'tenant', models.ForeignKey(related_name=b'+', to=b'exchange.ExchangeTenant'))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Group', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'backend_id', models.CharField(db_index=True, max_length=255)),
      (
       b'username', models.CharField(max_length=255)),
      (
       b'manager_email', models.EmailField(max_length=255)),
      (
       b'tenant', models.ForeignKey(related_name=b'+', to=b'exchange.ExchangeTenant'))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'User', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'backend_id', models.CharField(db_index=True, max_length=255)),
      (
       b'username', models.CharField(max_length=255)),
      (
       b'first_name', models.CharField(max_length=255)),
      (
       b'last_name', models.CharField(max_length=255)),
      (
       b'password', models.CharField(max_length=255)),
      (
       b'mailbox_size', models.PositiveSmallIntegerField(help_text=b'Maximum size of mailbox, MB')),
      (
       b'tenant', models.ForeignKey(related_name=b'+', to=b'exchange.ExchangeTenant'))], options={b'abstract': False}, bases=(
      models.Model,))]