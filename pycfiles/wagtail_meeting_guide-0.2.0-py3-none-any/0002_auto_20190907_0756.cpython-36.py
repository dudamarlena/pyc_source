# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tallen/projects/wagtail-meeting-guide/meeting_guide/migrations/0002_auto_20190907_0756.py
# Compiled at: 2019-12-27 18:00:05
# Size of source mod 2**32: 524 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('meeting_guide', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='meetingtype',
       options={'ordering': ['display_order', 'type_name']}),
     migrations.AddField(model_name='meetingtype',
       name='display_order',
       field=models.PositiveSmallIntegerField(default=100))]