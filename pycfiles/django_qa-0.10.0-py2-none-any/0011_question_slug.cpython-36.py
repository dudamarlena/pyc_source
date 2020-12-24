# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cristian/projects/python/django-qa/qa/migrations/0011_question_slug.py
# Compiled at: 2018-03-17 13:09:30
# Size of source mod 2**32: 810 bytes
from __future__ import unicode_literals
from django.db import migrations, models
from django.utils.text import slugify

def generate_slug(apps, schema_editor):
    MyModel = apps.get_model('qa', 'Question')
    for row in MyModel.objects.all():
        row.slug = slugify(row.title)
        row.save()


class Migration(migrations.Migration):
    dependencies = [
     ('qa', '0010_auto_20160919_2033')]
    operations = [
     migrations.AddField(model_name='question',
       name='slug',
       field=models.SlugField(default='', max_length=200),
       preserve_default=False),
     migrations.RunPython(generate_slug,
       reverse_code=(migrations.RunPython.noop))]