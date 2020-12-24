# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/migrations/0009_itservices_as_resource.py
# Compiled at: 2016-09-21 16:06:28
from __future__ import unicode_literals
from django.db import models, migrations
import django.db.models.deletion, django.utils.timezone, model_utils.fields, taggit.managers, django_fsm

class Migration(migrations.Migration):
    dependencies = [
     ('taggit', '0002_auto_20150616_2121'),
     ('nodeconductor_zabbix', '0008_add_itservice_trigger')]
    operations = [
     migrations.AddField(model_name=b'itservice', name=b'created', field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False), preserve_default=True),
     migrations.AddField(model_name=b'itservice', name=b'description', field=models.CharField(max_length=500, verbose_name=b'description', blank=True), preserve_default=True),
     migrations.AddField(model_name=b'itservice', name=b'error_message', field=models.TextField(blank=True), preserve_default=True),
     migrations.AddField(model_name=b'itservice', name=b'is_main', field=models.BooleanField(default=True, help_text=b'Main IT service SLA will be added to hosts resource as monitoring item.'), preserve_default=True),
     migrations.AddField(model_name=b'itservice', name=b'modified', field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False), preserve_default=True),
     migrations.AddField(model_name=b'itservice', name=b'service_project_link', field=models.ForeignKey(related_name=b'itservices', on_delete=django.db.models.deletion.PROTECT, default=1, to=b'nodeconductor_zabbix.ZabbixServiceProjectLink'), preserve_default=False),
     migrations.AddField(model_name=b'itservice', name=b'start_time', field=models.DateTimeField(null=True, blank=True), preserve_default=True),
     migrations.AddField(model_name=b'itservice', name=b'state', field=django_fsm.FSMIntegerField(default=1, help_text=b'WARNING! Should not be changed manually unless you really know what you are doing.', choices=[(1, 'Provisioning Scheduled'), (2, 'Provisioning'), (3, 'Online'), (4, 'Offline'), (5, 'Starting Scheduled'), (6, 'Starting'), (7, 'Stopping Scheduled'), (8, 'Stopping'), (9, 'Erred'), (10, 'Deletion Scheduled'), (11, 'Deleting'), (13, 'Resizing Scheduled'), (14, 'Resizing'), (15, 'Restarting Scheduled'), (16, 'Restarting')]), preserve_default=True),
     migrations.AddField(model_name=b'itservice', name=b'tags', field=taggit.managers.TaggableManager(to=b'taggit.Tag', through=b'taggit.TaggedItem', blank=True, help_text=b'A comma-separated list of tags.', verbose_name=b'Tags'), preserve_default=True),
     migrations.AlterField(model_name=b'itservice', name=b'backend_id', field=models.CharField(max_length=255, blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'itservice', name=b'host', field=models.ForeignKey(related_name=b'itservices', blank=True, to=b'nodeconductor_zabbix.Host', null=True), preserve_default=True),
     migrations.AlterUniqueTogether(name=b'itservice', unique_together=set([('host', 'is_main')])),
     migrations.RemoveField(model_name=b'itservice', name=b'settings')]