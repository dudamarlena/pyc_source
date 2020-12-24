# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/explore/migrations/0009_auto_20200420_1521.py
# Compiled at: 2020-05-05 16:46:09
# Size of source mod 2**32: 899 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('explore', '0008_corpus_parsed')]
    operations = [
     migrations.AlterField(model_name='corpus',
       name='language',
       field=models.ForeignKey(choices=[
      ('nl', 'Dutch'),
      ('en', 'English'),
      ('fr', 'French'),
      ('de', 'German'),
      ('el', 'Greek'),
      ('it', 'Italian'),
      ('pt', 'Portuguese'),
      ('es', 'Spanish')],
       null=True,
       on_delete=(django.db.models.deletion.SET_NULL),
       to='explore.Language'))]