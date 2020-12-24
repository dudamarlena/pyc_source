# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/migrations/0002_auto_20170126_0518.py
# Compiled at: 2017-10-20 11:35:08
from __future__ import unicode_literals
from django.db import migrations, models
import simplemde.fields

class Migration(migrations.Migration):
    dependencies = [
     ('composer', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'tile', name=b'markdown', field=simplemde.fields.SimpleMDEField(blank=True, null=True)),
     migrations.AlterField(model_name=b'slot', name=b'slot_name', field=models.CharField(help_text=b'Which base template slot should this be rendered in?', max_length=32)),
     migrations.AlterField(model_name=b'slot', name=b'url', field=models.CharField(db_index=True, default=b'^/$', help_text=b'Where on the site this slot will appear. This value\nmay be a regular expression and may be very complex. A simple example is\n^/about-us/, which means any URL starting with /about-us/ will have this slot.', max_length=100, verbose_name=b'URL')),
     migrations.AlterField(model_name=b'tile', name=b'style', field=models.CharField(blank=True, default=b'tile', help_text=b'The style of template that is used to render the item inside the tile if target is set.', max_length=200, null=True)),
     migrations.AlterField(model_name=b'tile', name=b'view_name', field=models.CharField(blank=True, help_text=b'A view to be rendered in this tile. This view is typically a snippet of a larger page. If you are unsure test and see if it works. If this value is set it has precedence over target.', max_length=200, null=True))]