# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/tests/test_stream/migrations/0001_initial.py
# Compiled at: 2015-01-17 16:40:50
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'StreamItemChild1', fields=[
      (
       b'streamitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'stream.StreamItem'))], options={b'abstract': False}, bases=('stream.streamitem', )),
     migrations.CreateModel(name=b'StreamItemChild2', fields=[
      (
       b'streamitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'stream.StreamItem'))], options={b'abstract': False}, bases=('stream.streamitem', ))]