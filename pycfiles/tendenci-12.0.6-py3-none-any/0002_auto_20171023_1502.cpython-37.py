# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/testimonials/migrations/0002_auto_20171023_1502.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 608 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('testimonials', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='testimonial',
       options={'ordering':[
       'position'], 
      'verbose_name':'Testimonial',  'verbose_name_plural':'Testimonials'}),
     migrations.AddField(model_name='testimonial',
       name='position',
       field=models.IntegerField(default=0, null=True, verbose_name='Position', blank=True))]