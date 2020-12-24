# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/notifications/migrations/0005_notificationsystem.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 700 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0004_auto_20190517_1651')]
    operations = [
     migrations.CreateModel(name='NotificationSystem',
       fields=[],
       options={'verbose_name':'Notification System', 
      'manager_inheritance_from_future':True, 
      'proxy':True, 
      'verbose_name_plural':'Notifications System', 
      'indexes':[]},
       bases=('notifications.notification', ))]