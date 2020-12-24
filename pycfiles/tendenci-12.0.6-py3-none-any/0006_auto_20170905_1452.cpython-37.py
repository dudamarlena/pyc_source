# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/videos/migrations/0006_auto_20170905_1452.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 568 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('videos', '0005_auto_20170608_1523')]
    operations = [
     migrations.AlterModelOptions(name='videotype',
       options={'ordering':('name', ), 
      'verbose_name_plural':'Video Types'}),
     migrations.AddField(model_name='video',
       name='position',
       field=models.IntegerField(default=0, null=True, verbose_name='Position', blank=True))]