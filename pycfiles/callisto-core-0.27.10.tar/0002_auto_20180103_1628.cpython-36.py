# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/accounts/migrations/0002_auto_20180103_1628.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 365 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('accounts', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='account',
       name='site_id',
       field=(models.PositiveSmallIntegerField()))]