# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/django_files_library/migrations/0001_initial.py
# Compiled at: 2018-02-10 07:51:58
# Size of source mod 2**32: 2572 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django_files_library.tools

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='File',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'uploaded_file', models.FileField(upload_to=(django_files_library.tools.unique_file_name))),
      (
       'original_name', models.CharField(blank=True, max_length=255, null=True)),
      (
       'name', models.CharField(blank=True, max_length=255, null=True)),
      (
       'description', models.CharField(blank=True, max_length=255, null=True)),
      (
       'created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
      (
       'created_by', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))]),
     migrations.CreateModel(name='Library',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(blank=True, max_length=255, null=True)),
      (
       'is_public', models.BooleanField(default=False)),
      (
       'created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On'))]),
     migrations.CreateModel(name='Permission',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
      (
       'access_level', models.CharField(choices=[('R', 'Read'), ('W', 'Write'), ('O', 'Owner')], max_length=1)),
      (
       'library', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='django_files_library.Library')),
      (
       'user', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))]),
     migrations.AddField(model_name='file',
       name='library',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='django_files_library.Library'))]