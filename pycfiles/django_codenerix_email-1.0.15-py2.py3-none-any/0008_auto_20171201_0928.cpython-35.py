# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_email/migrations/0008_auto_20171201_0928.py
# Compiled at: 2017-12-14 11:36:41
# Size of source mod 2**32: 731 bytes
from __future__ import unicode_literals
import codenerix.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_email', '0007_emailmessage_next_retry')]
    operations = [
     migrations.AlterField(model_name='emailtemplatetexten', name='body', field=codenerix.fields.WysiwygAngularField(blank=True, verbose_name='Body')),
     migrations.AlterField(model_name='emailtemplatetextes', name='body', field=codenerix.fields.WysiwygAngularField(blank=True, verbose_name='Body'))]