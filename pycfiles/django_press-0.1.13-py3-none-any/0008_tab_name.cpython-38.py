# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\migrations\0008_tab_name.py
# Compiled at: 2019-12-19 21:28:39
# Size of source mod 2**32: 420 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_press', '0007_contactcontent_success_page')]
    operations = [
     migrations.AddField(model_name='tab',
       name='name',
       field=models.CharField(max_length=50, null=True))]