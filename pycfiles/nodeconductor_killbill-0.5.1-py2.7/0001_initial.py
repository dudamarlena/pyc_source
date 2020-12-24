# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_killbill/migrations/0001_initial.py
# Compiled at: 2016-09-25 09:47:37
from __future__ import unicode_literals
from django.db import models, migrations
import nodeconductor.logging.loggers, nodeconductor.core.fields

class Migration(migrations.Migration):
    dependencies = [
     ('structure', '0026_add_error_message')]
    operations = [
     migrations.CreateModel(name=b'Invoice', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'amount', models.DecimalField(max_digits=9, decimal_places=2)),
      (
       b'date', models.DateField()),
      (
       b'pdf', models.FileField(null=True, upload_to=b'invoices', blank=True)),
      (
       b'usage_pdf', models.FileField(null=True, upload_to=b'invoices', blank=True)),
      (
       b'backend_id', models.CharField(max_length=255, blank=True)),
      (
       b'customer', models.ForeignKey(related_name=b'killbill_invoices', to=b'structure.Customer'))], options={b'abstract': False}, bases=(
      nodeconductor.logging.loggers.LoggableMixin, models.Model))]