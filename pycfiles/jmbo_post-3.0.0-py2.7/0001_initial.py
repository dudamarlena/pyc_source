# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/post/migrations/0001_initial.py
# Compiled at: 2017-07-03 11:37:50
from __future__ import unicode_literals
import simplemde.fields
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('jmbo', '0003_auto_20160530_1247')]
    operations = [
     migrations.CreateModel(name=b'Post', fields=[
      (
       b'modelbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'jmbo.ModelBase')),
      (
       b'content', simplemde.fields.SimpleMDEField(blank=True, null=True))], options={b'verbose_name': b'Post', 
        b'verbose_name_plural': b'Posts'}, bases=('jmbo.modelbase', ))]