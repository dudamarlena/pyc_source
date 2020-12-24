# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s.lihobabin/projects/protector/django-protector/protector/migrations/0002_auto_20160607_0827.py
# Compiled at: 2018-05-03 13:51:19
# Size of source mod 2**32: 1613 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('protector', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='genericglobalperm',
       name='content_type',
       field=models.ForeignKey(related_name='global_perms', default=1, verbose_name='content type', to='contenttypes.ContentType', on_delete=(models.CASCADE))),
     migrations.AlterField(model_name='genericglobalperm',
       name='permission',
       field=models.ForeignKey(verbose_name='permission', to='auth.Permission', on_delete=(models.CASCADE))),
     migrations.AlterField(model_name='genericusertogroup',
       name='group_content_type',
       field=models.ForeignKey(verbose_name='group content type', to='contenttypes.ContentType', on_delete=(models.CASCADE))),
     migrations.AlterField(model_name='genericusertogroup',
       name='group_id',
       field=models.PositiveIntegerField(verbose_name='group id')),
     migrations.AlterField(model_name='restriction',
       name='content_type',
       field=models.ForeignKey(verbose_name='content type', to='contenttypes.ContentType', on_delete=(models.CASCADE))),
     migrations.AlterField(model_name='restriction',
       name='object_id',
       field=models.PositiveIntegerField(verbose_name='object id'))]