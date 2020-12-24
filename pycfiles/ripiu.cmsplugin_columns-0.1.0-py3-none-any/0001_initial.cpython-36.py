# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/github/ripiu.cmsplugin_columns/ripiu/cmsplugin_columns/migrations/0001_initial.py
# Compiled at: 2017-09-30 19:39:34
# Size of source mod 2**32: 1043 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('cms', '0016_auto_20160608_1535')]
    operations = [
     migrations.CreateModel(name='LiquidColumnsPluginModel',
       fields=[
      (
       'cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, related_name='cmsplugin_columns_liquidcolumnspluginmodel', serialize=False, to='cms.CMSPlugin')),
      (
       'num_columns', models.IntegerField(default=2, help_text='How many columns for this section?', verbose_name='columns'))],
       options={'verbose_name':'Liquid columns', 
      'verbose_name_plural':'Liquid columns'},
       bases=('cms.cmsplugin', ))]