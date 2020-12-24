# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/philip/venvs/mezzanine-github/lib/python3.4/site-packages/mezzanine_slideshows/migrations/0001_initial.py
# Compiled at: 2015-05-29 22:16:14
# Size of source mod 2**32: 1073 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0002_auto_20141227_0224'),
     ('galleries', '0002_auto_20141227_0224')]
    operations = [
     migrations.CreateModel(name='Slideshow', fields=[
      (
       'id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
      (
       'slideshow_title', models.CharField(blank=True, help_text='A brief description of the slideshow', max_length=30)),
      (
       'slideshow_description', models.TextField(blank=True, help_text='A fuller description of the slideshow', max_length=100)),
      (
       'gallery', models.ForeignKey(to='galleries.Gallery')),
      (
       'page', models.OneToOneField(to='pages.RichTextPage'))], options={'verbose_name_plural': 'Slideshows', 
      'verbose_name': 'Slideshow'})]