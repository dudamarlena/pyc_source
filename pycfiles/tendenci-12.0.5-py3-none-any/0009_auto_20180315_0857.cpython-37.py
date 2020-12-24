# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/videos/migrations/0009_auto_20180315_0857.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 882 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('videos', '0008_auto_20170905_1509')]
    operations = [
     migrations.AlterField(model_name='video',
       name='category',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), to='videos.Category', null=True)),
     migrations.AlterField(model_name='video',
       name='slug',
       field=models.SlugField(unique=True, max_length=200, verbose_name='URL Path')),
     migrations.AlterField(model_name='video',
       name='video_type',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), blank=True, to='videos.VideoType', null=True))]