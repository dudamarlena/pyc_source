# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0008_auto_20150101_2320.py
# Compiled at: 2015-01-17 16:40:50
# Size of source mod 2**32: 1538 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0007_auto_20141219_1753')]
    operations = [
     migrations.AlterModelOptions(name='stream', options={'permissions': (('read', 'read'), ('write', 'write'), ('delete', 'delete'))}),
     migrations.AlterModelOptions(name='streamitem', options={'ordering': ['-publication_date'],  'permissions': (('read', 'read'), ('write', 'write'), ('delete', 'delete'))}),
     migrations.AlterField(model_name='itemcomment', name='status', field=models.CharField(default='awaiting_moderation', max_length=255, choices=[('published', 'Published'), ('awaiting_moderation', 'awaiting moderation'), ('disapproved', 'disapproved'), ('junk', 'junk')])),
     migrations.AlterField(model_name='stream', name='title', field=models.CharField(max_length=255, verbose_name='Title')),
     migrations.AlterField(model_name='streamitem', name='status', field=models.CharField(default='pub', max_length=5, choices=[('dra', 'Draft'), ('pub', 'Published')])),
     migrations.AlterField(model_name='streamitem', name='title', field=models.CharField(max_length=255, verbose_name='Title'))]