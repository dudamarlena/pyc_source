# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\migrations\0009_page_publish.py
# Compiled at: 2020-01-08 02:33:10
# Size of source mod 2**32: 425 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_press', '0008_tab_name')]
    operations = [
     migrations.AddField(model_name='page',
       name='publish',
       field=models.BooleanField(default=True, verbose_name='公開設定'))]