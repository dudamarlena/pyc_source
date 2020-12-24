# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/explore/migrations/0008_corpus_parsed.py
# Compiled at: 2020-05-05 16:46:09
# Size of source mod 2**32: 385 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('explore', '0007_auto_20191211_1501')]
    operations = [
     migrations.AddField(model_name='corpus',
       name='parsed',
       field=models.BooleanField(default=False))]