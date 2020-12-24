# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0004_auto_20181025_1537.py
# Compiled at: 2018-10-25 08:07:56
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0003_auto_20181025_1537'),
     ('bookmarks', '0001_initial'),
     ('books', '0002_booksegment'),
     ('reviews', '0002_basereviewsegment'),
     ('categories', '0002_category_pages'),
     ('sliders', '0005_auto_20181025_1537'),
     ('courses', '0003_coursecategory')]
    operations = [
     migrations.RemoveField(model_name=b'coursecategory', name=b'category_ptr'),
     migrations.DeleteModel(name=b'CourseCategory')]