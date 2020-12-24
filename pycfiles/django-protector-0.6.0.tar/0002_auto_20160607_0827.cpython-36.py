# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s.lihobabin/projects/protector/django-protector/protector/migrations/0002_auto_20160607_0827.py
# Compiled at: 2017-07-18 04:51:58
# Size of source mod 2**32: 1509 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('protector', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='genericglobalperm',
       name='content_type',
       field=models.ForeignKey(related_name='global_perms', default=1, verbose_name='content type', to='contenttypes.ContentType')),
     migrations.AlterField(model_name='genericglobalperm',
       name='permission',
       field=models.ForeignKey(verbose_name='permission', to='auth.Permission')),
     migrations.AlterField(model_name='genericusertogroup',
       name='group_content_type',
       field=models.ForeignKey(verbose_name='group content type', to='contenttypes.ContentType')),
     migrations.AlterField(model_name='genericusertogroup',
       name='group_id',
       field=models.PositiveIntegerField(verbose_name='group id')),
     migrations.AlterField(model_name='restriction',
       name='content_type',
       field=models.ForeignKey(verbose_name='content type', to='contenttypes.ContentType')),
     migrations.AlterField(model_name='restriction',
       name='object_id',
       field=models.PositiveIntegerField(verbose_name='object id'))]