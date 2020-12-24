# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/videos/migrations/0004_auto_20161020_1638.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 485 bytes
from django.db import migrations

def populate_release_dt(apps, schema_editor):
    Video = apps.get_model('videos', 'Video')
    for video in Video.objects.all():
        if not video.release_dt:
            video.release_dt = video.create_dt
            video.save()


class Migration(migrations.Migration):
    dependencies = [
     ('videos', '0003_video_release_dt')]
    operations = [
     migrations.RunPython(populate_release_dt)]