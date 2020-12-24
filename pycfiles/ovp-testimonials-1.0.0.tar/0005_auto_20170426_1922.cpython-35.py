# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-testimonials/ovp_testimonials/migrations/0005_auto_20170426_1922.py
# Compiled at: 2017-04-26 15:22:34
# Size of source mod 2**32: 612 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_testimonials', '0004_auto_20170426_1838')]
    operations = [
     migrations.AlterField(model_name='testimonial', name='user', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]