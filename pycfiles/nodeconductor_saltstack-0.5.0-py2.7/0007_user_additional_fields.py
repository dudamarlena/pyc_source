# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/migrations/0007_user_additional_fields.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations
import nodeconductor_saltstack.exchange.validators

class Migration(migrations.Migration):
    dependencies = [
     ('exchange', '0006_group_manager_foreign_key')]
    operations = [
     migrations.AddField(model_name=b'user', name=b'company', field=models.CharField(max_length=255, blank=True), preserve_default=True),
     migrations.AddField(model_name=b'user', name=b'department', field=models.CharField(max_length=255, blank=True), preserve_default=True),
     migrations.AddField(model_name=b'user', name=b'manager', field=models.ForeignKey(blank=True, to=b'exchange.User', null=True), preserve_default=True),
     migrations.AddField(model_name=b'user', name=b'office', field=models.CharField(max_length=255, blank=True), preserve_default=True),
     migrations.AddField(model_name=b'user', name=b'phone', field=models.CharField(max_length=255, blank=True), preserve_default=True),
     migrations.AddField(model_name=b'user', name=b'title', field=models.CharField(max_length=255, blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'exchangetenant', name=b'domain', field=models.CharField(max_length=255, validators=[nodeconductor_saltstack.exchange.validators.domain_validator]), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'username', field=models.CharField(unique=True, max_length=255), preserve_default=True)]