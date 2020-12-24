# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0014_questionpage_to_page_3.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 795 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0013_questionpage_to_page_2')]
    operations = [
     migrations.AlterField(model_name='formquestion',
       name='page',
       field=models.ForeignKey(null=True,
       on_delete=(models.deletion.SET_NULL),
       to='wizard_builder.Page')),
     migrations.RemoveField(model_name='questionpage', name='pagebase_ptr'),
     migrations.RemoveField(model_name='questionpage', name='sites'),
     migrations.DeleteModel(name='QuestionPage'),
     migrations.DeleteModel(name='PageBase')]