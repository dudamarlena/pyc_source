# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/case_studies/migrations/0002_auto_20180724_1325.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 586 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('case_studies', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='image',
       name='file_ptr',
       field=models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, related_name='case_studies_image_related', serialize=False, to='files.File'))]