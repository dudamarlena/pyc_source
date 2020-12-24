# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/cosales/migrations/0005_auto_20190315_1347.py
# Compiled at: 2019-03-15 06:17:43
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('notifiesme', '0001_initial'),
     ('sliders', '0004_sliderimage'),
     ('counters', '0002_auto_20190115_1425'),
     ('segments', '0012_auto_20181214_1330'),
     ('notifications', '0001_initial'),
     ('reviews', '0004_reviewsummary_percentage'),
     ('bookmarks', '0002_auto_20181026_1745'),
     ('buttons', '0006_auto_20190120_1724'),
     ('cosales', '0004_auto_20190315_1340')]
    operations = [
     migrations.RemoveField(model_name=b'cosalehistory', name=b'basemodel_ptr'),
     migrations.RemoveField(model_name=b'cosalehistory', name=b'cosale_obj'),
     migrations.RemoveField(model_name=b'cosale', name=b'status'),
     migrations.DeleteModel(name=b'CoSaleHistory')]