# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/wagtail_feeds/migrations/0003_auto_20180130_0818.py
# Compiled at: 2018-05-08 10:24:10
# Size of source mod 2**32: 2665 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('wagtail_feeds', '0002_rssfeedssettings_feed_image_in_content')]
    operations = [
     migrations.AlterField(model_name='rssfeedssettings',
       name='feed_app_label',
       field=models.CharField(blank=True, help_text='blog App whose Feed is to be generated', max_length=255, null=True)),
     migrations.AlterField(model_name='rssfeedssettings',
       name='feed_author_email',
       field=models.EmailField(blank=True, help_text='Email of author', max_length=255, null=True)),
     migrations.AlterField(model_name='rssfeedssettings',
       name='feed_author_link',
       field=models.URLField(blank=True, help_text='Link of author', max_length=255, null=True)),
     migrations.AlterField(model_name='rssfeedssettings',
       name='feed_description',
       field=models.CharField(blank=True, help_text='Description of field', max_length=255, null=True)),
     migrations.AlterField(model_name='rssfeedssettings',
       name='feed_image_in_content',
       field=models.BooleanField(default=True, help_text='Add feed image to content encoded field')),
     migrations.AlterField(model_name='rssfeedssettings',
       name='feed_item_content_field',
       field=models.CharField(blank=True, help_text='Content Field for feed item', max_length=255, null=True)),
     migrations.AlterField(model_name='rssfeedssettings',
       name='feed_item_description_field',
       field=models.CharField(blank=True, help_text='Description field for feed item', max_length=255, null=True)),
     migrations.AlterField(model_name='rssfeedssettings',
       name='feed_link',
       field=models.URLField(blank=True, help_text='link for Feed', max_length=255, null=True)),
     migrations.AlterField(model_name='rssfeedssettings',
       name='feed_model_name',
       field=models.CharField(blank=True, help_text='Model to be used for feed generation', max_length=255, null=True)),
     migrations.AlterField(model_name='rssfeedssettings',
       name='feed_title',
       field=models.CharField(blank=True, help_text='Title of Feed', max_length=255, null=True))]