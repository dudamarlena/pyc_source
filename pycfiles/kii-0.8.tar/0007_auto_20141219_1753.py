# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0007_auto_20141219_1753.py
# Compiled at: 2015-01-17 16:40:50
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0006_auto_20141217_1757')]
    operations = [
     migrations.AlterModelOptions(name=b'stream', options={b'permissions': (('read', 'permissions.read'), ('write', 'permissions.write'), ('delete', 'permissions.delete'))}),
     migrations.AlterModelOptions(name=b'streamitem', options={b'ordering': [b'-publication_date'], b'permissions': (('read', 'permissions.read'), ('write', 'permissions.write'), ('delete', 'permissions.delete'))}),
     migrations.RemoveField(model_name=b'itemcomment', name=b'publication_date'),
     migrations.AlterField(model_name=b'itemcomment', name=b'status', field=models.CharField(default=b'awaiting_moderation', max_length=255, choices=[('published', 'published'), ('awaiting_moderation', 'awaiting moderation'), ('disapproved', 'disapproved'), ('junk', 'junk')]))]