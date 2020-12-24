# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0027_sentfullreport.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 479 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0026_auto_20171122_1446')]
    operations = [
     migrations.CreateModel(name='SentFullReport',
       fields=[],
       options={'proxy':True, 
      'indexes':[]},
       bases=('delivery.newsentfullreport', ))]