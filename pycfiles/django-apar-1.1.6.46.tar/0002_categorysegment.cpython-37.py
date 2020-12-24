# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/categories/migrations/0002_categorysegment.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 845 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0002_auto_20181026_1745'),
     ('categories', '0001_initial')]
    operations = [
     migrations.CreateModel(name='CategorySegment',
       fields=[
      (
       'basesegment_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='segments.BaseSegment'))],
       options={'verbose_name':'Category Segment', 
      'verbose_name_plural':'Category Segments'},
       bases=('segments.basesegment', ))]