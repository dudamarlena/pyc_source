# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/wp_importer/migrations/0001_initial.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1211 bytes
from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('files', '0001_initial')]
    operations = [
     migrations.CreateModel(name='AssociatedFile',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'post_id', models.IntegerField()),
      (
       'file', models.ForeignKey(to='files.File', on_delete=(django.db.models.deletion.CASCADE)))]),
     migrations.CreateModel(name='BlogImport',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'blog_import_date', models.DateTimeField(auto_now_add=True)),
      (
       'blog', models.FileField(upload_to='blogimport')),
      (
       'author', models.ForeignKey(to=(settings.AUTH_USER_MODEL), on_delete=(django.db.models.deletion.CASCADE)))])]