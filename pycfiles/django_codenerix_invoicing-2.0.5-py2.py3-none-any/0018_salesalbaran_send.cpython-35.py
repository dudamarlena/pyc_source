# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0018_salesalbaran_send.py
# Compiled at: 2018-05-03 06:55:10
# Size of source mod 2**32: 493 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0017_cashdiary_cashmovement')]
    operations = [
     migrations.AddField(model_name='salesalbaran', name='send', field=models.BooleanField(default=False, verbose_name='Send'))]