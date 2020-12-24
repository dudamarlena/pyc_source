# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-sparkle-external/django-sparkle-external/sparkle/migrations/0002_auto_20140701_1935.py
# Compiled at: 2014-07-01 07:35:06
# Size of source mod 2**32: 1481 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sparkle', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Channel', fields=[
      (
       'id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
      (
       'name', models.CharField(verbose_name='name', max_length=50)),
      (
       'slug', models.SlugField(verbose_name='slug', unique=True))], options={'verbose_name': 'channel', 
      'verbose_name_plural': 'channels'}, bases=(
      models.Model,)),
     migrations.AlterModelOptions(name='version', options={'ordering': ('-publish_at', ),  'verbose_name': 'version',  'verbose_name_plural': 'versions',  'get_latest_by': 'version'}),
     migrations.AddField(model_name='application', name='default_channel', field=models.ForeignKey(null=True, verbose_name='default channel', to='sparkle.Channel'), preserve_default=True),
     migrations.AddField(model_name='version', name='channels', field=models.ManyToManyField(verbose_name='channels', to='sparkle.Channel'), preserve_default=True)]