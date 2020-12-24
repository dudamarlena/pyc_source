# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/asso/diacamma/event/migrations/0006_article_nomember.py
# Compiled at: 2020-03-20 14:11:02
# Size of source mod 2**32: 984 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('invoice', '0007_storage'),
     ('event', '0005_invoice_change')]
    operations = [
     migrations.AddField(model_name='event', name='default_article_nomember', field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='eventnomember', to='invoice.Article', verbose_name='default article (no member)')),
     migrations.AlterField(model_name='event', name='default_article', field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='event', to='invoice.Article', verbose_name='default article (member)'))]