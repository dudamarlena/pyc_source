# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/workspaces/workspace_django/django-celerybeat-status/celerybeat_status/admin.py
# Compiled at: 2018-01-27 05:47:23
# Size of source mod 2**32: 102 bytes
from django.contrib.admin.sites import AdminSite
AdminSite.index_template = 'admin/custom_index.html'