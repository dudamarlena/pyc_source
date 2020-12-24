# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0008_auto_20170626_1456.py
# Compiled at: 2017-06-26 14:56:02
# Size of source mod 2**32: 750 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0007_resource_sha1')]
    operations = [
     migrations.AlterField(model_name='location', name='domain', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neurobank.Domain')),
     migrations.AlterField(model_name='location', name='resource', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neurobank.Resource'))]