# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/videos/migrations/0008_auto_20170905_1509.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 538 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('videos', '0007_auto_20170905_1455')]
    operations = [
     migrations.AlterModelOptions(name='video',
       options={'ordering':('position', ), 
      'verbose_name':'Videos',  'verbose_name_plural':'Videos',  'permissions':(('view_video', 'Can view video'), )}),
     migrations.RemoveField(model_name='video',
       name='ordering')]