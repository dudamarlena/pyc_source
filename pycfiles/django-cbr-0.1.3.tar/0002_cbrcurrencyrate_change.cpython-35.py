# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-licyilu1/django-cbr/cbr/migrations/0002_cbrcurrencyrate_change.py
# Compiled at: 2017-08-28 23:32:16
# Size of source mod 2**32: 534 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cbr', '0001_initial')]
    operations = [
     migrations.AddField(model_name='cbrcurrencyrate', name='change', field=models.DecimalField(decimal_places=4, default=0, max_digits=10, verbose_name='Change'), preserve_default=False)]