# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/videos/migrations/0007_auto_20170905_1455.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 494 bytes
from django.db import migrations

def assign_position(apps, schema_editor):
    """
    Assign value from ordering to position
    """
    Video = apps.get_model('videos', 'Video')
    for video in Video.objects.all():
        video.position = video.ordering
        video.save()


class Migration(migrations.Migration):
    dependencies = [
     ('videos', '0006_auto_20170905_1452')]
    operations = [
     migrations.RunPython(assign_position)]