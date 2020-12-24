# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/migrations/0002_category.py
# Compiled at: 2016-09-30 00:56:02
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('helpcenter', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Category', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(db_index=True, help_text=b"A category's title is restricted to 200 characters.", max_length=200, verbose_name=b'Category Title')),
      (
       b'parent', models.ForeignKey(blank=True, help_text=b'Categories can be nested as deep as you would like.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'helpcenter.Category', verbose_name=b'Parent Category'))])]