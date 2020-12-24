# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/directories/migrations/0003_auto_20171013_1041.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 629 bytes
from django.db import migrations, models
import tendenci.libs.tinymce.models

class Migration(migrations.Migration):
    dependencies = [
     ('directories', '0002_auto_20150804_1545')]
    operations = [
     migrations.AlterField(model_name='directory',
       name='body',
       field=tendenci.libs.tinymce.models.HTMLField(verbose_name='Description')),
     migrations.AlterField(model_name='directory',
       name='headline',
       field=models.CharField(max_length=200, verbose_name='Name', blank=True))]