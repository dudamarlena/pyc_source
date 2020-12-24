# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/stories/migrations/0003_auto_20180315_0857.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 459 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('stories', '0002_story_video_embed_url')]
    operations = [
     migrations.AlterField(model_name='story',
       name='video_embed_url',
       field=models.URLField(help_text='Embed URL for a Youtube or Vimeo video', null=True, verbose_name='Embed URL', blank=True))]