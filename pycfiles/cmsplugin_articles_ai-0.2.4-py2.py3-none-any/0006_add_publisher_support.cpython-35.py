# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/migrations/0006_add_publisher_support.py
# Compiled at: 2017-07-21 05:10:28
# Size of source mod 2**32: 1213 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles_ai', '0005_make_tag_slug_field_unique')]
    operations = [
     migrations.AddField(model_name='article', name='publisher_is_draft', field=models.BooleanField(default=True, editable=False, db_index=True)),
     migrations.AddField(model_name='article', name='publisher_linked', field=models.OneToOneField(null=True, related_name='publisher_draft', to='cmsplugin_articles_ai.Article', on_delete=django.db.models.deletion.SET_NULL, editable=False)),
     migrations.AddField(model_name='article', name='publisher_modified_at', field=models.DateTimeField(default=django.utils.timezone.now, editable=False)),
     migrations.AddField(model_name='article', name='publisher_published_at', field=models.DateTimeField(null=True, editable=False))]