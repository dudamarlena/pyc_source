# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/snappion_backend/avishan/migrations/0003_requesttrackexecinfo.py
# Compiled at: 2020-02-15 16:09:26
# Size of source mod 2**32: 1027 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('avishan', '0002_translatablechar')]
    operations = [
     migrations.CreateModel(name='RequestTrackExecInfo',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=255)),
      (
       'start_time', models.DateTimeField(blank=True, null=True)),
      (
       'end_time', models.DateTimeField(blank=True, null=True)),
      (
       'milliseconds', models.FloatField(blank=True, default=None, null=True)),
      (
       'request_track', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='exec_infos', to='avishan.RequestTrack'))],
       options={'abstract': False})]