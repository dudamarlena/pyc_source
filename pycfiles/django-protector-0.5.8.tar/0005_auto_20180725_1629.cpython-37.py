# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s.lihobabin/projects/protector/django-protector/protector/migrations/0005_auto_20180725_1629.py
# Compiled at: 2018-07-26 13:32:58
# Size of source mod 2**32: 1575 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('protector', '0004_auto_20170906_1215')]
    operations = [
     migrations.AlterModelOptions(name='permissioninfo',
       options={'verbose_name':'permission info', 
      'verbose_name_plural':'permissions info'}),
     migrations.AlterField(model_name='genericglobalperm',
       name='content_type',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='global_perms', to='contenttypes.ContentType', verbose_name='content type')),
     migrations.AlterField(model_name='ownertopermission',
       name='content_type',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='restriction_group_relations', to='contenttypes.ContentType', verbose_name='object type')),
     migrations.AlterField(model_name='ownertopermission',
       name='object_id',
       field=models.PositiveIntegerField(null=True, verbose_name='object id')),
     migrations.AlterField(model_name='permissioninfo',
       name='permission',
       field=models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), related_name='info', to='auth.Permission'))]