# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii-blog/kii_blog/migrations/0001_initial.py
# Compiled at: 2014-12-16 11:40:40
from __future__ import unicode_literals
from django.db import models, migrations
import kii.base_models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0003_auto_20141216_1441')]
    operations = [
     migrations.CreateModel(name=b'Entry', fields=[
      (
       b'streamitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'stream.StreamItem')),
      (
       b'slug', kii.base_models.fields.SlugField(populate_from=('title', ), editable=False, blank=True))], options={b'abstract': False}, bases=('stream.streamitem', ))]