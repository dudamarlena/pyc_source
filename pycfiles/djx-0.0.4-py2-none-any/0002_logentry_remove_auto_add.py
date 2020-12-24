# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/admin/migrations/0002_logentry_remove_auto_add.py
# Compiled at: 2019-02-14 00:35:15
from __future__ import unicode_literals
from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'logentry', name=b'action_time', field=models.DateTimeField(verbose_name=b'action time', default=timezone.now, editable=False))]