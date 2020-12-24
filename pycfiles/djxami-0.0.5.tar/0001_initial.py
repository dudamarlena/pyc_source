# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/xacce/addit/Projects/inventory/venv/local/lib/python2.7/site-packages/djxami/migrations/0001_initial.py
# Compiled at: 2016-02-08 09:41:09
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.db.migrations.migration import SwappableTuple

def swappable_dependency_latest(value):
    """
    Turns a setting value into a dependency.
    """
    return SwappableTuple((value.split(b'.', 1)[0], b'__latest__'), value)


class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('contenttypes', '__latest__'),
     ('auth', '__latest__'),
     swappable_dependency_latest(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Message', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'viewed', models.BooleanField(default=False)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'mark_as_viewed_at', models.DateTimeField(blank=True, null=True)),
      (
       b'globally', models.BooleanField(default=False)),
      (
       b'object_id', models.PositiveIntegerField(blank=True, null=True)),
      (
       b'content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'contenttypes.ContentType'))]),
     migrations.CreateModel(name=b'MessageToGroup', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'auth.Group')),
      (
       b'message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'djxami.Message'))]),
     migrations.CreateModel(name=b'MessageToUser', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'viewed', models.BooleanField(default=False)),
      (
       b'message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'message_to_user', to=b'djxami.Message')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'messages', to=settings.AUTH_USER_MODEL))]),
     migrations.AddField(model_name=b'message', name=b'groups', field=models.ManyToManyField(through=b'djxami.MessageToGroup', to=b'auth.Group')),
     migrations.AddField(model_name=b'message', name=b'users', field=models.ManyToManyField(through=b'djxami.MessageToUser', to=settings.AUTH_USER_MODEL)),
     migrations.AlterIndexTogether(name=b'message', index_together=set([('content_type', 'object_id')]))]