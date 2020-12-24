# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/testimonials/migrations/0004_auto_20180315_0857.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 539 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('testimonials', '0003_auto_20171023_1527')]
    operations = [
     migrations.AlterField(model_name='testimonial',
       name='image',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), default=None, to='testimonials.TestimonialPhoto', help_text='Photo for this testimonial.', null=True))]