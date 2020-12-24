# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/tests/test_stream/migrations/0001_initial.py
# Compiled at: 2015-01-17 16:40:50
# Size of source mod 2**32: 1005 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0001_initial')]
    operations = [
     migrations.CreateModel(name='StreamItemChild1', fields=[
      (
       'streamitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='stream.StreamItem'))], options={'abstract': False}, bases=('stream.streamitem', )),
     migrations.CreateModel(name='StreamItemChild2', fields=[
      (
       'streamitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='stream.StreamItem'))], options={'abstract': False}, bases=('stream.streamitem', ))]