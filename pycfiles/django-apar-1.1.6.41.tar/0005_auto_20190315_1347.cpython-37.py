# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/cosales/migrations/0005_auto_20190315_1347.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1036 bytes
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
     migrations.RemoveField(model_name='cosalehistory',
       name='basemodel_ptr'),
     migrations.RemoveField(model_name='cosalehistory',
       name='cosale_obj'),
     migrations.RemoveField(model_name='cosale',
       name='status'),
     migrations.DeleteModel(name='CoSaleHistory')]