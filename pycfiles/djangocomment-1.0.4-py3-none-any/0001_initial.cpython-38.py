# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangocomment\src\djangocomment\migrations\0001_initial.py
# Compiled at: 2020-02-22 01:50:33
# Size of source mod 2**32: 1171 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('contenttypes', '0002_remove_content_type_name')]
    operations = [
     migrations.CreateModel(name='CommentModel',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'object_id', models.PositiveIntegerField(blank=True, null=True)),
      (
       'content', models.TextField(blank=True, null=True)),
      (
       'datetime', models.DateTimeField(auto_now_add=True)),
      (
       'author', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL))),
      (
       'content_type', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='contenttypes.ContentType'))])]