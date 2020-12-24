# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/migrations/0005_blogpost_category.py
# Compiled at: 2018-08-06 04:08:22
# Size of source mod 2**32: 597 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('django_blogposts', '0004_categories')]
    operations = [
     migrations.AddField(model_name='blogpost', name='category', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_blogposts.Categories', verbose_name='category'))]