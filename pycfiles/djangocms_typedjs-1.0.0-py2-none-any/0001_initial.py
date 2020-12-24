# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/life-website-env/life-website/website/djangocms_typedjs/migrations/0001_initial.py
# Compiled at: 2016-07-18 08:58:26
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('cms', '0015_auto_20160421_0000')]
    operations = [
     migrations.CreateModel(name=b'TypedJS', fields=[
      (
       b'cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'cms.CMSPlugin')),
      (
       b'name', models.CharField(max_length=50, verbose_name=b'name')),
      (
       b'blinking_cursor', models.BooleanField(default=True, verbose_name=b'blinking cursor')),
      (
       b'json_config', models.TextField(blank=True, help_text=b'The JSON object passed to Typed.js. For more info <a target="_blank" href="https://github.com/mattboldt/typed.js/">click here</a>', null=True, verbose_name=b'JSON config'))], options={b'verbose_name': b'Typed.js', 
        b'verbose_name_plural': b'Typed.js'}, bases=('cms.cmsplugin', ))]