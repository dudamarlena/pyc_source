# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-testimonials/ovp_testimonials/migrations/0003_auto_20170426_1833.py
# Compiled at: 2017-04-26 14:33:38
# Size of source mod 2**32: 409 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_testimonials', '0002_testimonials')]
    operations = [
     migrations.RenameModel(old_name='Testimonials', new_name='Testimonial')]