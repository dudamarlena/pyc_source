# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled/NearBeach/migrations/0005_document_permission_whiteboard_id.py
# Compiled at: 2020-05-06 03:21:35
# Size of source mod 2**32: 520 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('NearBeach', '0004_auto_20200329_1013')]
    operations = [
     migrations.AddField(model_name='document_permission',
       name='whiteboard_id',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='NearBeach.whiteboard'))]