# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-testimonials/ovp_testimonials/migrations/0006_auto_20170426_1929.py
# Compiled at: 2017-04-26 15:29:02
# Size of source mod 2**32: 753 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_testimonials', '0005_auto_20170426_1922')]
    operations = [
     migrations.RemoveField(model_name='testimonial', name='deleted'),
     migrations.RemoveField(model_name='testimonial', name='deleted_date'),
     migrations.RemoveField(model_name='testimonial', name='modified_date'),
     migrations.RemoveField(model_name='testimonial', name='published_date')]