# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-audiofield/audiofield/migrations/0002_auto_20180121_0750.py
# Compiled at: 2018-01-28 09:58:08
import audiofield.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('audiofield', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='audiofile', name='audio_file', field=audiofield.fields.AudioField(blank=True, upload_to='upload/audiofiles', verbose_name='audio file'))]