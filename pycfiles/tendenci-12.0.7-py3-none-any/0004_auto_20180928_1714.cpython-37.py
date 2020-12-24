# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/projects/migrations/0004_auto_20180928_1714.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 534 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('projects', '0003_auto_20180928_1713')]
    operations = [
     migrations.AlterField(model_name='documents',
       name='doc_type',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='projects.DocumentType'))]