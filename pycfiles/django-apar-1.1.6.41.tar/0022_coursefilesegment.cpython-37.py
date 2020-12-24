# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0022_coursefilesegment.py
# Compiled at: 2020-03-16 03:47:17
# Size of source mod 2**32: 834 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0013_auto_20190615_1430'),
     ('courses', '0021_auto_20190714_1639')]
    operations = [
     migrations.CreateModel(name='CourseFileSegment',
       fields=[
      (
       'basesegment_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='segments.BaseSegment'))],
       options={'verbose_name':'Course File Segment', 
      'verbose_name_plural':'Course Files Segments'},
       bases=('segments.basesegment', ))]