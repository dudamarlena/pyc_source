# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/plugins/tombstone/migrations/0001_initial.py
# Compiled at: 2015-02-18 15:30:56
# Size of source mod 2**32: 1299 bytes
from __future__ import unicode_literals
from django.db import models, migrations
import cms.models.pluginmodel

class Migration(migrations.Migration):
    dependencies = [
     ('content', '__first__'),
     ('cms', '0003_auto_20140926_2347')]
    operations = [
     migrations.CreateModel(name='TombstonePlugin', fields=[
      (
       'cmsplugin_ptr', models.OneToOneField(primary_key=True, to='cms.CMSPlugin', parent_link=True, auto_created=True, serialize=False)),
      (
       'promo_text', models.CharField(max_length=255, blank=True, null=True)),
      (
       'highlighted_text', models.CharField(help_text='Phrases matching this text will be highlighted in red when appearing in headlines.', max_length=255, blank=True, null=True)),
      (
       'image', models.ImageField(upload_to=cms.models.pluginmodel.CMSPlugin.get_media_path, verbose_name='image', blank=True, null=True)),
      (
       'image_alt_text', models.CharField(max_length=255, blank=True, null=True)),
      (
       'article', models.ForeignKey(to='content.Article', blank=True, null=True))], options={'abstract': False}, bases=('cms.cmsplugin', ))]