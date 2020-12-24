# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0013_auto_20190326_2256.py
# Compiled at: 2019-03-26 21:56:37
# Size of source mod 2**32: 454 bytes
from django.db import migrations
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0012_user_token')]
    operations = [
     migrations.AlterField(model_name='user',
       name='name',
       field=djangoplus.db.models.fields.CharField(blank=True, max_length=100, verbose_name='Nome'))]