# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0011_auto_20150104_1751.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 490 bytes
from __future__ import unicode_literals
from django.db import models, migrations
import kii.base_models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0010_stream_slug')]
    operations = [
     migrations.AlterField(model_name='stream', name='slug', field=kii.base_models.fields.SlugField(editable=False, populate_from=('title', ), blank=True, unique=True))]