# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0010_basesegment_pages.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 591 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0002_page_english_title'),
     ('segments', '0009_remove_basesegment_pages')]
    operations = [
     migrations.AddField(model_name='basesegment',
       name='pages',
       field=models.ManyToManyField(blank=True, related_name='segment_pages', through='segments.PageSort', to='pages.Page', verbose_name='\\u0635\\u0641\\u062d\\u0647'))]