# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/articles/migrations/0005_auto_20180718_1202.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 650 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('files', '0001_initial'),
     ('articles', '0004_auto_20180315_1839')]
    operations = [
     migrations.AddField(model_name='article',
       name='thumbnail',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), to='files.File', help_text='The thumbnail image can be used on your homepage or sidebar if it is setup in your theme. The thumbnail image will not display on the news page.', null=True))]