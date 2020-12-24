# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_products/migrations/0007_auto_20180123_1316.py
# Compiled at: 2018-02-02 06:33:32
# Size of source mod 2**32: 929 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0006_auto_20180118_1126')]
    operations = [
     migrations.AddField(model_name='productunique', name='stock_locked', field=models.FloatField(default=0, editable=False, verbose_name='Stock locked')),
     migrations.AddField(model_name='productunique', name='stock_original', field=models.FloatField(default=0, editable=False, verbose_name='Stock original')),
     migrations.AlterField(model_name='productunique', name='stock_real', field=models.FloatField(default=0, editable=False, verbose_name='Stock real'))]