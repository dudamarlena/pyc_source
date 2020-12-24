# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0009_auto_20170626_1458.py
# Compiled at: 2017-06-26 14:58:55
# Size of source mod 2**32: 576 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0008_auto_20170626_1456')]
    operations = [
     migrations.AlterField(model_name='resource', name='sha1', field=models.CharField(blank=True, help_text='specify only for resources whose contents must not change (i.e., sources)', max_length=40, null=True, unique=True))]