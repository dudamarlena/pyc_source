# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s.lihobabin/projects/protector/django-protector/protector/migrations/0002_auto_20160607_0827.py
# Compiled at: 2018-05-03 13:51:19
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('protector', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'genericglobalperm', name=b'content_type', field=models.ForeignKey(related_name=b'global_perms', default=1, verbose_name=b'content type', to=b'contenttypes.ContentType', on_delete=models.CASCADE)),
     migrations.AlterField(model_name=b'genericglobalperm', name=b'permission', field=models.ForeignKey(verbose_name=b'permission', to=b'auth.Permission', on_delete=models.CASCADE)),
     migrations.AlterField(model_name=b'genericusertogroup', name=b'group_content_type', field=models.ForeignKey(verbose_name=b'group content type', to=b'contenttypes.ContentType', on_delete=models.CASCADE)),
     migrations.AlterField(model_name=b'genericusertogroup', name=b'group_id', field=models.PositiveIntegerField(verbose_name=b'group id')),
     migrations.AlterField(model_name=b'restriction', name=b'content_type', field=models.ForeignKey(verbose_name=b'content type', to=b'contenttypes.ContentType', on_delete=models.CASCADE)),
     migrations.AlterField(model_name=b'restriction', name=b'object_id', field=models.PositiveIntegerField(verbose_name=b'object id'))]