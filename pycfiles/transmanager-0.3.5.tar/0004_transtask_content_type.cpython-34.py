# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/migrations/0004_transtask_content_type.py
# Compiled at: 2016-06-01 06:08:22
# Size of source mod 2**32: 536 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     ('transmanager', '0003_auto_20160513_2151')]
    operations = [
     migrations.AddField(model_name='transtask', name='content_type', field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True, verbose_name='Modelo'))]