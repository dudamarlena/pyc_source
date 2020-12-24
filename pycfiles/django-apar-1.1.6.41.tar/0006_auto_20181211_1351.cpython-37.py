# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0006_auto_20181211_1351.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1533 bytes
from django.db import migrations, models
import tagulous.models.fields, tagulous.models.models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0005_basemodel_is_show_only_for_super_user')]
    operations = [
     migrations.CreateModel(name='Tagulous_BaseModel_tags',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=255, unique=True)),
      (
       'slug', models.SlugField()),
      (
       'count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
      (
       'protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0'))],
       options={'ordering':('name', ), 
      'abstract':False},
       bases=(
      tagulous.models.models.BaseTagModel, models.Model)),
     migrations.AlterUniqueTogether(name='tagulous_basemodel_tags',
       unique_together=(set([('slug', )]))),
     migrations.AddField(model_name='basemodel',
       name='tags',
       field=tagulous.models.fields.TagField(_set_tag_meta=True, help_text='Enter a comma-separated tag string', to='basemodels.Tagulous_BaseModel_tags'))]