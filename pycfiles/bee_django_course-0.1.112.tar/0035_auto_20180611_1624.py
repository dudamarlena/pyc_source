# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0035_auto_20180611_1624.py
# Compiled at: 2018-06-26 00:36:23
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0034_auto_20180521_1400')]
    operations = [
     migrations.AlterModelTable(name=b'sectionattach', table=b'bee_django_course_section_attach'),
     migrations.AlterModelTable(name=b'sectionvideo', table=b'bee_django_course_section_video'),
     migrations.AlterModelTable(name=b'userassignment', table=b'bee_django_course_user_assignment'),
     migrations.AlterModelTable(name=b'userassignmentimage', table=b'bee_django_course_user_assignment_image'),
     migrations.AlterModelTable(name=b'usercourse', table=b'bee_django_course_user_course'),
     migrations.AlterModelTable(name=b'usercoursesection', table=b'bee_django_course_user_course_section'),
     migrations.AlterModelTable(name=b'userimage', table=b'bee_django_course_user_image')]