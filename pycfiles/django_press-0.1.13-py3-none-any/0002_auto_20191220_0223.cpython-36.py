# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\migrations\0002_auto_20191220_0223.py
# Compiled at: 2019-12-19 18:56:48
# Size of source mod 2**32: 533 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('django_press', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='contactcontent',
       name='form',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.PROTECT), to='django_press.BaseInquiry', verbose_name='問い合わせ系'))]