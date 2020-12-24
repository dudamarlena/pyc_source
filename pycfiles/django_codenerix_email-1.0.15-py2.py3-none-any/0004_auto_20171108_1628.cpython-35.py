# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_email/migrations/0004_auto_20171108_1628.py
# Compiled at: 2017-11-10 07:59:46
# Size of source mod 2**32: 486 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_email', '0003_auto_20170921_1206')]
    operations = [
     migrations.AlterField(model_name='emailattachment', name='path', field=models.FileField(upload_to='', verbose_name='Path'))]