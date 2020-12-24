# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s.lihobabin/projects/protector/django-protector/protector/migrations/0005_auto_20180725_1629.py
# Compiled at: 2018-07-26 13:32:58
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('protector', '0004_auto_20170906_1215')]
    operations = [
     migrations.AlterModelOptions(name=b'permissioninfo', options={b'verbose_name': b'permission info', b'verbose_name_plural': b'permissions info'}),
     migrations.AlterField(model_name=b'genericglobalperm', name=b'content_type', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'global_perms', to=b'contenttypes.ContentType', verbose_name=b'content type')),
     migrations.AlterField(model_name=b'ownertopermission', name=b'content_type', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'restriction_group_relations', to=b'contenttypes.ContentType', verbose_name=b'object type')),
     migrations.AlterField(model_name=b'ownertopermission', name=b'object_id', field=models.PositiveIntegerField(null=True, verbose_name=b'object id')),
     migrations.AlterField(model_name=b'permissioninfo', name=b'permission', field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name=b'info', to=b'auth.Permission'))]