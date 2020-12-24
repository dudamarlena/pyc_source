# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/migrations/0008_add_itservice_trigger.py
# Compiled at: 2016-09-21 16:06:28
from __future__ import unicode_literals
from django.db import models, migrations
import nodeconductor.core.fields, nodeconductor.core.models, nodeconductor.core.validators, nodeconductor.logging.loggers

class Migration(migrations.Migration):
    dependencies = [
     ('taggit', '0002_auto_20150616_2121'),
     ('structure', '0032_make_options_optional'),
     ('nodeconductor_zabbix', '0007_add_sla')]
    operations = [
     migrations.CreateModel(name=b'ITService', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'backend_id', models.CharField(max_length=255, db_index=True)),
      (
       b'settings', models.ForeignKey(related_name=b'+', to=b'structure.ServiceSettings')),
      (
       b'agreed_sla', models.DecimalField(null=True, max_digits=6, decimal_places=4, blank=True)),
      (
       b'algorithm', models.PositiveSmallIntegerField(default=0, choices=[(0, 'do not calculate'), (1, 'problem, if at least one child has a problem'), (2, 'problem, if all children have problems')])),
      (
       b'sort_order', models.PositiveSmallIntegerField(default=1)),
      (
       b'host', models.ForeignKey(on_delete=models.deletion.PROTECT, blank=True, to=b'nodeconductor_zabbix.Host', null=True)),
      (
       b'backend_trigger_id', models.CharField(max_length=64, null=True, blank=True))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.AlterUniqueTogether(name=b'itservice', unique_together=set([('settings', 'backend_id')])),
     migrations.CreateModel(name=b'Trigger', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=255, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'backend_id', models.CharField(max_length=255, db_index=True)),
      (
       b'settings', models.ForeignKey(related_name=b'+', to=b'structure.ServiceSettings')),
      (
       b'template', models.ForeignKey(related_name=b'triggers', to=b'nodeconductor_zabbix.Template'))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.AlterUniqueTogether(name=b'trigger', unique_together=set([('settings', 'backend_id')])),
     migrations.AddField(model_name=b'itservice', name=b'trigger', field=models.ForeignKey(blank=True, to=b'nodeconductor_zabbix.Trigger', null=True), preserve_default=False),
     migrations.RemoveField(model_name=b'host', name=b'agreed_sla'),
     migrations.RemoveField(model_name=b'host', name=b'service_id'),
     migrations.RemoveField(model_name=b'host', name=b'trigger_id'),
     migrations.AlterField(model_name=b'item', name=b'name', field=models.CharField(max_length=255), preserve_default=True),
     migrations.AddField(model_name=b'slahistory', name=b'itservice', field=models.ForeignKey(to=b'nodeconductor_zabbix.ITService'), preserve_default=False),
     migrations.AlterUniqueTogether(name=b'slahistory', unique_together=set([('itservice', 'period')])),
     migrations.RemoveField(model_name=b'slahistory', name=b'host')]