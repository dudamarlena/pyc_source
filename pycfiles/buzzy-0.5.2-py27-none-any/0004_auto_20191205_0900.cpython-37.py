# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/explore/migrations/0004_auto_20191205_0900.py
# Compiled at: 2020-05-05 16:46:09
# Size of source mod 2**32: 539 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('explore', '0003_auto_20191202_2136')]
    operations = [
     migrations.AddField(model_name='corpus',
       name='initial_query',
       field=models.TextField(null=True)),
     migrations.AddField(model_name='corpus',
       name='initial_table',
       field=models.TextField(null=True))]