# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/coupons/migrations/0002_auto_20190618_1638.py
# Compiled at: 2019-06-18 08:08:38
# Size of source mod 2**32: 460 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('coupons', '0001_initial')]
    operations = [
     migrations.DeleteModel(name='CouponForAllUser'),
     migrations.DeleteModel(name='CouponForCoustomUser'),
     migrations.DeleteModel(name='CouponForLimitedUser')]