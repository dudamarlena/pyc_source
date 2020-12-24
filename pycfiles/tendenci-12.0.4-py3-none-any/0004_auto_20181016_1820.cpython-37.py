# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/invoices/migrations/0004_auto_20181016_1820.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1023 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('invoices', '0003_auto_20181008_1243')]
    operations = [
     migrations.AddField(model_name='invoice',
       name='void_date',
       field=models.DateTimeField(null=True)),
     migrations.AddField(model_name='invoice',
       name='void_reason',
       field=models.TextField(blank=True, default='', max_length=200, verbose_name='Reason to void')),
     migrations.AddField(model_name='invoice',
       name='voided_by',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='invoice_voided_by', to=(settings.AUTH_USER_MODEL)))]