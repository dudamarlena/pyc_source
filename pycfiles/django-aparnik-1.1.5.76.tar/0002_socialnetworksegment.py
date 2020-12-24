# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/socials/migrations/0002_socialnetworksegment.py
# Compiled at: 2018-12-03 11:15:34
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0002_auto_20181026_1745'),
     ('socials', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'SocialNetworkSegment', fields=[
      (
       b'basesegment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'segments.BaseSegment'))], options={b'verbose_name': b'Social Segment', 
        b'manager_inheritance_from_future': True, 
        b'verbose_name_plural': b'Social Segments'}, bases=('segments.basesegment', ))]