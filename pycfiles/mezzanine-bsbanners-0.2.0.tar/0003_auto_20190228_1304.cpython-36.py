# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/alan/projects/mldemo-po/mezzanine_bsbanners/migrations/0003_auto_20190228_1304.py
# Compiled at: 2019-02-28 08:04:41
# Size of source mod 2**32: 1147 bytes
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('mezzanine_bsbanners', '0002_auto_20161102_1400')]
    operations = [
     migrations.AddField(model_name='banners',
       name='carouseltransition',
       field=models.CharField(choices=[('slide', 'Slide'), ('fade', 'Fade')], default='slide', help_text='Animate slides with a slide or fade transition.', max_length=5, verbose_name='Carousel transition')),
     migrations.AlterField(model_name='banners',
       name='slug',
       field=models.CharField(blank=True, default=(django.utils.timezone.now), help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, verbose_name='URL'),
       preserve_default=False),
     migrations.AlterField(model_name='slides',
       name='image',
       field=models.FileField(blank=True, max_length=255, null=True, upload_to='slides', verbose_name='Image'))]