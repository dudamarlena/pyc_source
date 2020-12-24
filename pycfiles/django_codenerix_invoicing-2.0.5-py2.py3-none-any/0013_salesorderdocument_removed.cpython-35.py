# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0013_salesorderdocument_removed.py
# Compiled at: 2018-02-16 08:44:37
# Size of source mod 2**32: 517 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0012_auto_20180201_1212')]
    operations = [
     migrations.AddField(model_name='salesorderdocument', name='removed', field=models.BooleanField(default=False, editable=False, verbose_name='Removed'))]