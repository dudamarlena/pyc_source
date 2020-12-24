# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/testimonials/migrations/0003_auto_20171023_1527.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 539 bytes
from django.db import migrations

def assign_position(apps, schema_editor):
    Testimonial = apps.get_model('testimonials', 'Testimonial')
    for i, t in enumerate(Testimonial.objects.all().order_by('create_dt')):
        t.position = i
        t.save()


class Migration(migrations.Migration):
    dependencies = [
     ('testimonials', '0002_auto_20171023_1502')]
    operations = [
     migrations.RunPython(assign_position)]