# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/craig.williams/.virtualenvs/test-trans/lib/python2.7/site-packages/mezzanine_smartling/migrations/0001_initial.py
# Compiled at: 2015-09-17 00:02:34
from __future__ import unicode_literals
from django.db import models, migrations
import mezzanine_smartling.models

class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0003_auto_20150527_1555'),
     ('sites', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'SmartlingTranslation', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'page_uri', models.CharField(max_length=1024)),
      (
       b'locale', models.CharField(max_length=1024)),
      (
       b'json_doc', mezzanine_smartling.models.LongJSONField(default=dict)),
      (
       b'created', models.DateTimeField(auto_now_add=True)),
      (
       b'approved', models.BooleanField(default=False)),
      (
       b'site', models.ForeignKey(related_name=b'smartlingtranslation_site', editable=False, to=b'sites.Site'))]),
     migrations.CreateModel(name=b'TestModel', fields=[
      (
       b'page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'pages.Page')),
      (
       b'rel_canonical', models.CharField(max_length=2048, blank=True)),
      (
       b'compact_header', models.BooleanField(default=False)),
      (
       b'hero_logo_image_alt', models.CharField(max_length=512, verbose_name=b'Image Alt Tag', blank=True))], options={b'ordering': ('_order', )}, bases=('pages.page', ))]