# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/ripiu.cmsplugin_lasagna/ripiu/cmsplugin_lasagna/migrations/0002_auto_20180102_1701.py
# Compiled at: 2018-01-02 11:01:46
# Size of source mod 2**32: 1618 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('cms', '0016_auto_20160608_1535'),
     ('cmsplugin_lasagna', '0001_initial')]
    operations = [
     migrations.CreateModel(name='ImageAnchorModifierPlugin',
       fields=[
      (
       'cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, related_name='cmsplugin_lasagna_imageanchormodifierplugin', serialize=False, to='cms.CMSPlugin')),
      (
       'anchor_point', models.CharField(blank=True, choices=[('center top', 'North'), ('right top', 'North-east'), ('right center', 'East'), ('right bottom', 'South-east'), ('center bottom', 'South'), ('left bottom', 'South-west'), ('left center', 'West'), ('left top', 'North-west'), ('center center', 'Middle')], default='', max_length=15, verbose_name='anchor point'))],
       options={'verbose_name':'Image anchor modifier', 
      'verbose_name_plural':'Image anchor modifiers'},
       bases=('cms.cmsplugin', )),
     migrations.AlterField(model_name='verticalalignmentmodifierplugin',
       name='alignment',
       field=models.PositiveSmallIntegerField(choices=[(0, 'top'), ('center center', 'middle'), (2, 'bottom')], default=0, verbose_name='alignment'))]