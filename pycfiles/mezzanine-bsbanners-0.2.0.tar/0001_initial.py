# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/alan/projects/mldemo-po/mezzanine_bsbanners/migrations/0001_initial.py
# Compiled at: 2018-11-16 08:38:15
from __future__ import unicode_literals
from django.db import models, migrations
import mezzanine.core.fields

class Migration(migrations.Migration):
    dependencies = [
     ('sites', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Banners', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'title', models.CharField(max_length=500, verbose_name=b'Title')),
      (
       b'slug', models.CharField(help_text=b'Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name=b'URL', blank=True)),
      (
       b'bannertype', models.SmallIntegerField(default=1, choices=[(1, 'Carousel'), (2, 'Jumbotron')])),
      (
       b'ctachevron', models.CharField(default=b'none', help_text=b'Add a chevron to call to action buttons', max_length=5, verbose_name=b'Button chevrons', choices=[('none', 'None'), ('left', 'Left'), ('right', 'Right')])),
      (
       b'buttonsize', models.CharField(default=b'default', help_text=b'Size of call to action buttons', max_length=7, verbose_name=b'Button size', choices=[('lg', 'Large'), ('default', 'Default'), ('sm', 'Small'), ('xs', 'Extra small')])),
      (
       b'interval', models.IntegerField(default=5000, help_text=b'The amount of time (in milliseconds) to delay between automatically cycling an item', verbose_name=b'interval')),
      (
       b'wrap', models.BooleanField(default=True, help_text=b'Whether the carousel should cycle continuously or have hard stops', verbose_name=b'wrap')),
      (
       b'pause', models.BooleanField(default=True, help_text=b'Pauses the cycling of the carousel on mouseenter and resumes the cycling of the carousel on mouseleave', verbose_name=b'pause')),
      (
       b'showindicators', models.BooleanField(default=True, verbose_name=b'Show indicators')),
      (
       b'animate', models.BooleanField(default=True, verbose_name=b'Animate transitions')),
      (
       b'status', models.SmallIntegerField(default=2, help_text=b'With Draft chosen, will only be shown for admin users on the site.', verbose_name=b'Status', choices=[(1, 'Draft'), (2, 'Published')])),
      (
       b'site', models.ForeignKey(editable=False, to=b'sites.Site', on_delete=models.CASCADE))], options={b'ordering': [
                    b'title'], 
        b'verbose_name': b'Banner', 
        b'verbose_name_plural': b'Banners'}),
     migrations.CreateModel(name=b'Slides', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'content', mezzanine.core.fields.RichTextField(verbose_name=b'Content')),
      (
       b'title', models.CharField(help_text=b'Slide/Jumbotron title', max_length=200, verbose_name=b'Title')),
      (
       b'show_title', models.BooleanField(default=True, help_text=b'If checked, show slide/jumbotron title.', verbose_name=b'Show title')),
      (
       b'cta', models.CharField(help_text=b'Text used for the call to action button', max_length=200, null=True, verbose_name=b'Call to action', blank=True)),
      (
       b'link_url', models.CharField(help_text=b'Link for the image and call to action button', max_length=200, null=True, verbose_name=b'Link', blank=True)),
      (
       b'buttontype', models.CharField(default=b'default', help_text=b'Call to action button type (colour)', max_length=7, verbose_name=b'Button type', choices=[('default', 'default'), ('primary', 'primary'), ('success', 'success'), ('info', 'info'), ('warning', 'warning'), ('danger', 'danger')])),
      (
       b'image', models.FileField(max_length=255, upload_to=b'slides/', null=True, verbose_name=b'Image', blank=True)),
      (
       b'status', models.SmallIntegerField(default=2, help_text=b'With Draft chosen, will only be shown for admin users on the site.', verbose_name=b'Status', choices=[(1, 'Draft'), (2, 'Published')])),
      (
       b'sort_order', models.SmallIntegerField(editable=False)),
      (
       b'banner', models.ForeignKey(to=b'mezzanine_bsbanners.Banners', on_delete=models.CASCADE))], options={b'ordering': [
                    b'sort_order'], 
        b'verbose_name': b'Slide', 
        b'verbose_name_plural': b'Slides'})]