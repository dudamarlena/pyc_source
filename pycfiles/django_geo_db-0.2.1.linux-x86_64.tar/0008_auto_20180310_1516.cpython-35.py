# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/migrations/0008_auto_20180310_1516.py
# Compiled at: 2018-03-10 10:16:41
# Size of source mod 2**32: 1045 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_geo_db', '0007_auto_20180310_0603')]
    operations = [
     migrations.AlterModelOptions(name='locationmaptype', options={'ordering': ('type', )}),
     migrations.AddField(model_name='locationmap', name='map_file_url', field=models.URLField(default=''), preserve_default=False),
     migrations.AlterField(model_name='locationmaptype', name='type', field=models.CharField(max_length=30, unique=True)),
     migrations.RemoveField(model_name='locationmap', name='file'),
     migrations.AlterUniqueTogether(name='locationmap', unique_together=set([('type', 'location')]))]