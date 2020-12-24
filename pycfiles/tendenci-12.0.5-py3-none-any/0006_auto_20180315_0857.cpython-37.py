# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/news/migrations/0006_auto_20180315_0857.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 841 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('news', '0005_auto_20160701_1627')]
    operations = [
     migrations.AlterField(model_name='news',
       name='meta',
       field=models.OneToOneField(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='meta.Meta')),
     migrations.AlterField(model_name='news',
       name='thumbnail',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), default=None, to='news.NewsImage', help_text='The thumbnail image can be used on your homepage or sidebar if it is setup in your theme. The thumbnail image will not display on the news page.', null=True))]