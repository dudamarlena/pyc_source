# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangocomment\src\djangocomment\migrations\0002_auto_20200317_0631.py
# Compiled at: 2020-03-16 21:01:52
# Size of source mod 2**32: 422 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djangocomment', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='commentmodel',
       options={'ordering':[
       '-pk'], 
      'verbose_name':'Comment',  'verbose_name_plural':'Comments'})]