# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0010_stream_slug.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 831 bytes
from __future__ import unicode_literals
from django.db import models, migrations
import kii.base_models.fields

def set_stream_slug(apps, schema_editor):
    stream_model = apps.get_model('stream', 'Stream')
    for stream in stream_model.objects.all():
        stream.slug = stream.title
        stream_model.objects.filter(pk=stream.pk).update(slug=stream.title)


class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0009_auto_20150104_1331')]
    operations = [
     migrations.AddField(model_name='stream', name='slug', field=kii.base_models.fields.SlugField(populate_from=('title', ), null=True, editable=False, blank=True), preserve_default=True),
     migrations.RunPython(set_stream_slug)]