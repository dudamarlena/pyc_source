# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/promotion/migrations/0005_auto_20150528_1434.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 525 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('promotion', '0004_auto_20150403_1549')]
    operations = [
     migrations.AlterField(model_name='pzoneoperation', name='polymorphic_ctype', field=models.ForeignKey(related_name='polymorphic_promotion.pzoneoperation_set+', editable=False, to='contenttypes.ContentType', null=True))]