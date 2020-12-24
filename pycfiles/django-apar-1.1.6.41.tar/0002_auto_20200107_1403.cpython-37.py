# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/aboutus/migrations/0002_auto_20200107_1403.py
# Compiled at: 2020-03-03 06:09:02
# Size of source mod 2**32: 445 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aboutus', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='information',
       name='short_blogs',
       field=models.ManyToManyField(blank=True, to='shortblogs.ShortBlog', verbose_name='Content Segment'))]