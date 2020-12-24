# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/liveblog/migrations/0003_auto_20160825_1459.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 396 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('liveblog', '0002_liveblogresponse_internal_name')]
    operations = [
     migrations.AlterModelOptions(name='liveblogresponse', options={'ordering': ['ordering']})]