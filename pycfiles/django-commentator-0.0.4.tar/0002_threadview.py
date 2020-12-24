# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/smidth/GitHub/django-commentator/commentator/migrations/0002_threadview.py
# Compiled at: 2015-03-18 05:49:53
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('commentator', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'ThreadView', fields=[
      (
       b'id',
       models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'timestamp',
       models.DateTimeField(db_index=True, null=True, blank=True)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'updated_at', models.DateTimeField(auto_now=True)),
      (
       b'thread',
       models.ForeignKey(verbose_name=b'Thread', to=b'commentator.Thread')),
      (
       b'user',
       models.ForeignKey(verbose_name=b'User', to=settings.AUTH_USER_MODEL))], options={b'ordering': ('thread', 'created_at'), 
        b'db_table': b'commentaror_threadview', 
        b'verbose_name': b'View', 
        b'verbose_name_plural': b'Views'}, bases=(
      models.Model,))]