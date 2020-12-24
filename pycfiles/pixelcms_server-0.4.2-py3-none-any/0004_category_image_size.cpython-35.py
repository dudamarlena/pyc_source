# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/content/migrations/0004_category_image_size.py
# Compiled at: 2016-11-20 17:45:38
# Size of source mod 2**32: 998 bytes
from __future__ import unicode_literals
import cms.common.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('content', '0003_auto_20161120_2334')]
    operations = [
     migrations.AddField(model_name='category', name='image_size', field=cms.common.fields.FilebrowserVersionField(choices=[('1col', '1 column (65x37)'), ('2cols', '2 columns (160x90)'), ('3cols', '3 columns (255x143)'), ('4cols', '4 columns (350x197)'), ('5cols', '5 columns (445x250)'), ('6cols', '6 columns (540x304)'), ('7cols', '7 columns (635x357)'), ('8cols', '8 columns (730x411)'), ('9cols', '9 columns (825x464)'), ('10cols', '10 columns (920x518)'), ('11cols', '11 columns (1015x571)'), ('12cols', '12 columns (1110x624)'), ('fullhd', 'Full HD (1920x1080)')], default='3cols', max_length=255, verbose_name='image size'))]