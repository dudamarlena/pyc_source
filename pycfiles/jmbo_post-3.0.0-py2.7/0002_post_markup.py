# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/post/migrations/0002_post_markup.py
# Compiled at: 2017-07-03 11:37:50
from __future__ import unicode_literals
import pypandoc
from django.db import migrations, models

def html_to_markdown(apps, schema_editor):
    Post = apps.get_model(b'post', b'post')
    for obj in Post.objects.all():
        if obj.content:
            obj.markdown = pypandoc.convert(obj.content, b'md', format=b'html')
            obj.save()


class Migration(migrations.Migration):
    dependencies = [
     ('post', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'post', name=b'markdown', field=models.TextField(blank=True, null=True)),
     migrations.RunPython(html_to_markdown, reverse_code=lambda a, b: None)]