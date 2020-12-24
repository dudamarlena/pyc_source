# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/life-website-env/life-website/website/website/apps/djangocms_background_media/migrations/0001_initial.py
# Compiled at: 2016-06-27 05:07:46
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, filer.fields.image

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('cms', '0015_auto_20160421_0000'),
     ('filer', '0004_auto_20160328_1434')]
    operations = [
     migrations.CreateModel(name=b'BackgroundMedia', fields=[
      (
       b'cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'cms.CMSPlugin')),
      (
       b'name', models.CharField(max_length=50, verbose_name=b'name')),
      (
       b'height', models.CharField(default=b'100%', help_text=b'height in pixels or %', max_length=10, verbose_name=b'container height')),
      (
       b'add_style', models.BooleanField(default=True, help_text=b'link default style sheet', verbose_name=b'add style')),
      (
       b'overlay', models.CharField(blank=True, help_text=b'to add a css overlay enter the colour of the overlay, e.g. rgba(0,0,0,0.7)', max_length=25, null=True, verbose_name=b'overlay')),
      (
       b'image_position', models.CharField(default=b'center center', help_text=b'the css position of the image', max_length=50, verbose_name=b'image position')),
      (
       b'video_mp4', models.FileField(blank=True, help_text=b'Video in the mp4 format', null=True, upload_to=b'videos/djangocms_bg_media', verbose_name=b'video mp4')),
      (
       b'video_ogv', models.FileField(blank=True, help_text=b'Video in the ogv format', null=True, upload_to=b'videos/djangocms_bg_media', verbose_name=b'video ogv')),
      (
       b'video_webm', models.FileField(blank=True, help_text=b'Video in the webm format', null=True, upload_to=b'videos/djangocms_bg_media', verbose_name=b'video ogv')),
      (
       b'vide_json_config', models.TextField(blank=True, help_text=b'the optional json object for the vide config. Click <a href="https://github.com/VodkaBears/Vide" target="_blank"> here</a> for more info', null=True, verbose_name=b'vide js json config')),
      (
       b'image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'image', to=b'filer.Image', verbose_name=b'image')),
      (
       b'video_poster', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'filer.Image', verbose_name=b'video poster'))], options={b'verbose_name': b'Background Media', 
        b'verbose_name_plural': b'Background Media'}, bases=('cms.cmsplugin', ))]