# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0030_newsentmatchreport_proxysentmatchreport.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1114 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0029_auto_20171122_1448')]
    operations = [
     migrations.CreateModel(name='NewSentMatchReport',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'sent', models.DateTimeField(auto_now_add=True)),
      (
       'to_address', models.TextField(null=True)),
      (
       'reports', models.ManyToManyField(to='delivery.MatchReport'))]),
     migrations.CreateModel(name='ProxySentMatchReport',
       fields=[],
       options={'proxy':True, 
      'indexes':[]},
       bases=('delivery.newsentmatchreport', ))]