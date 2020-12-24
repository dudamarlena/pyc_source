# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_cms/migrations/0008_auto_20171123_1019.py
# Compiled at: 2017-11-28 07:16:52
# Size of source mod 2**32: 698 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_cms', '0007_auto_20171115_1546')]
    operations = [
     migrations.AlterField(model_name='sliderelement', name='show_title', field=models.BooleanField(default=False, verbose_name='Show title')),
     migrations.AlterField(model_name='staticheaderelement', name='show_title', field=models.BooleanField(default=False, verbose_name='Show title'))]