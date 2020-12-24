# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0012_user_token.py
# Compiled at: 2019-03-14 17:14:33
# Size of source mod 2**32: 461 bytes
from django.db import migrations
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0011_auto_20190312_1716')]
    operations = [
     migrations.AddField(model_name='user',
       name='token',
       field=djangoplus.db.models.fields.CharField(max_length=255, null=True, verbose_name='Token'))]