# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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