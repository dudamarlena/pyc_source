# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/socials/migrations/0003_socialnetwork2.py
# Compiled at: 2018-12-03 04:20:42
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0004_filefield_title'),
     ('basemodels', '0004_auto_20181103_2233'),
     ('socials', '0002_socialnetworksegment')]
    operations = [
     migrations.CreateModel(name=b'SocialNetwork2', fields=[
      (
       b'basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'basemodels.BaseModel')),
      (
       b'link', models.URLField(max_length=255, verbose_name=b'Link')),
      (
       b'title', models.CharField(default=None, max_length=31, verbose_name=b'Title')),
      (
       b'android_app_shortcut', models.CharField(blank=True, max_length=200, null=True, verbose_name=b'Android shortcut')),
      (
       b'ios_app_shortcut', models.CharField(blank=True, max_length=200, null=True, verbose_name=b'iOS shortcut')),
      (
       b'icon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'filefields.FileField', verbose_name=b'Icon'))], options={b'verbose_name': b'Social Network', 
        b'manager_inheritance_from_future': True, 
        b'verbose_name_plural': b'Social Networks'}, bases=('basemodels.basemodel', ))]