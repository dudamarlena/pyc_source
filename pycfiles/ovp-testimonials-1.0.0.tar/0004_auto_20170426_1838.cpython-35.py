# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-testimonials/ovp_testimonials/migrations/0004_auto_20170426_1838.py
# Compiled at: 2017-04-26 14:38:01
# Size of source mod 2**32: 1535 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_testimonials', '0003_auto_20170426_1833')]
    operations = [
     migrations.AddField(model_name='testimonial', name='created_date', field=models.DateTimeField(auto_now_add=True, default=None, verbose_name='Created date'), preserve_default=False),
     migrations.AddField(model_name='testimonial', name='deleted', field=models.BooleanField(default=False, verbose_name='Deleted')),
     migrations.AddField(model_name='testimonial', name='deleted_date', field=models.DateTimeField(blank=True, null=True, verbose_name='Deleted date')),
     migrations.AddField(model_name='testimonial', name='modified_date', field=models.DateTimeField(auto_now=True, verbose_name='Modified date')),
     migrations.AddField(model_name='testimonial', name='published', field=models.BooleanField(default=False, verbose_name='Published')),
     migrations.AddField(model_name='testimonial', name='published_date', field=models.DateTimeField(blank=True, null=True, verbose_name='Published date'))]