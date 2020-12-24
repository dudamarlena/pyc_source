# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangocomment\src\djangocomment\migrations\0003_commentmodel_parent.py
# Compiled at: 2020-04-16 23:13:56
# Size of source mod 2**32: 533 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djangocomment', '0002_auto_20200317_0631')]
    operations = [
     migrations.AddField(model_name='commentmodel',
       name='parent',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='djangocomment.CommentModel'))]