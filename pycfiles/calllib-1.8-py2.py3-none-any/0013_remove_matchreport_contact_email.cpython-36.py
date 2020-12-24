# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0013_remove_matchreport_contact_email.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 355 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0012_auto_20170814_0137')]
    operations = [
     migrations.RemoveField(model_name='matchreport', name='contact_email')]