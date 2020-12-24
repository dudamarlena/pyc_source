# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/migrations/0009_auto_20200331_2041.py
# Compiled at: 2020-04-21 05:34:55
# Size of source mod 2**32: 1059 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('avishan', '0008_auto_20200312_1444')]
    operations = [
     migrations.CreateModel(name='Activity',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=255)),
      (
       'date_created', models.DateTimeField(auto_now_add=True)),
      (
       'request_track', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='avishan.RequestTrack')),
      (
       'user_user_group', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='avishan.UserUserGroup'))],
       options={'abstract': False}),
     migrations.DeleteModel(name='RequestTrackMessage')]