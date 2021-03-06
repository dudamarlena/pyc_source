# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/forums/migrations/0002_slugs_optional.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 747 bytes
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('forums', '0001_initial')]
    operations = [
     migrations.AddField(model_name='category',
       name='slug',
       field=models.SlugField(max_length=255, verbose_name='Slug', blank=True)),
     migrations.AddField(model_name='forum',
       name='slug',
       field=models.SlugField(max_length=255, verbose_name='Slug', blank=True)),
     migrations.AddField(model_name='topic',
       name='slug',
       field=models.SlugField(max_length=255, verbose_name='Slug', blank=True))]