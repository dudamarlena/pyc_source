# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_wiki/migrations/0001_initial.py
# Compiled at: 2019-08-30 04:44:02
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Classify', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, verbose_name=b'分类'))], options={b'db_table': b'bee_django_wiki_classify', 
        b'permissions': (('view_all_classify', '可以查看分类'), )}),
     migrations.CreateModel(name=b'Topic', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=180, verbose_name=b'标题')),
      (
       b'detail', models.TextField(verbose_name=b'详情')),
      (
       b'tag', models.CharField(max_length=180, null=True, verbose_name=b'标签')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'updated_at', models.DateTimeField(auto_now=True)),
      (
       b'order_by', models.IntegerField(default=0, null=True, verbose_name=b'排序')),
      (
       b'view_group', models.TextField(null=True, verbose_name=b'可观看的用户组')),
      (
       b'classfify', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_wiki.Classify', verbose_name=b'分类'))], options={b'ordering': [
                    b'-updated_at'], 
        b'db_table': b'bee_django_wiki_topic', 
        b'permissions': (('view_all_topic', '查看所有主题'), )})]