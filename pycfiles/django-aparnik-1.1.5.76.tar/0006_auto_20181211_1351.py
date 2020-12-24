# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0006_auto_20181211_1351.py
# Compiled at: 2018-12-11 08:51:05
from __future__ import unicode_literals
from django.db import migrations, models
import tagulous.models.fields, tagulous.models.models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0005_basemodel_is_show_only_for_super_user')]
    operations = [
     migrations.CreateModel(name=b'Tagulous_BaseModel_tags', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=255, unique=True)),
      (
       b'slug', models.SlugField()),
      (
       b'count', models.IntegerField(default=0, help_text=b'Internal counter of how many times this tag is in use')),
      (
       b'protected', models.BooleanField(default=False, help_text=b'Will not be deleted when the count reaches 0'))], options={b'ordering': ('name', ), 
        b'abstract': False}, bases=(
      tagulous.models.models.BaseTagModel, models.Model)),
     migrations.AlterUniqueTogether(name=b'tagulous_basemodel_tags', unique_together=set([('slug', )])),
     migrations.AddField(model_name=b'basemodel', name=b'tags', field=tagulous.models.fields.TagField(_set_tag_meta=True, help_text=b'Enter a comma-separated tag string', to=b'basemodels.Tagulous_BaseModel_tags'))]