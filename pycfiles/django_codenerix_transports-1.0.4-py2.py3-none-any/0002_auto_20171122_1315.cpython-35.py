# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_transports/migrations/0002_auto_20171122_1315.py
# Compiled at: 2017-11-22 12:04:33
# Size of source mod 2**32: 2144 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_transports', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='transportrequest', name='answer', field=models.TextField(blank=True, null=True, verbose_name='Answer')),
     migrations.AlterField(model_name='transportrequest', name='answer_date', field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Answer date')),
     migrations.AlterField(model_name='transportrequest', name='cancelled', field=models.BooleanField(default=False, verbose_name='Cancelled')),
     migrations.AlterField(model_name='transportrequest', name='error_txt', field=models.TextField(blank=True, null=True, verbose_name='Error Text')),
     migrations.AlterField(model_name='transportrequest', name='notes', field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Notes')),
     migrations.AlterField(model_name='transportrequest', name='platform', field=models.CharField(max_length=20, verbose_name='Platform')),
     migrations.AlterField(model_name='transportrequest', name='ref', field=models.CharField(default=None, max_length=15, null=True, verbose_name='Reference')),
     migrations.AlterField(model_name='transportrequest', name='request', field=models.TextField(blank=True, null=True, verbose_name='Request')),
     migrations.AlterField(model_name='transportrequest', name='request_date', field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Request date'))]