# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/migrations/0007_auto_20160301_1014.py
# Compiled at: 2018-08-06 04:08:22
# Size of source mod 2**32: 518 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_blogposts', '0006_auto_20160301_0905')]
    operations = [
     migrations.AddField(model_name='blogpost', name='tags', field=models.ManyToManyField(blank=True, null=True, to='django_blogposts.Tags', verbose_name='tags'))]