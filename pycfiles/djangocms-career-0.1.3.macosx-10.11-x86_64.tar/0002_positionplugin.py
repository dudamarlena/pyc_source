# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/cms-sample/dev_packages/djangocms-career/djangocms_career/migrations/0002_positionplugin.py
# Compiled at: 2016-04-18 05:27:38
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cms', '0013_urlconfrevision'),
     ('djangocms_career', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'PositionPlugin', fields=[
      (
       b'cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'cms.CMSPlugin')),
      (
       b'post', models.ForeignKey(to=b'djangocms_career.Position'))], options={b'abstract': False}, bases=('cms.cmsplugin', ))]