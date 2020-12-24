# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/django_files_library/admin.py
# Compiled at: 2018-02-10 07:51:58
# Size of source mod 2**32: 188 bytes
from django.contrib import admin
from django_files_library.models import Library, Permission, File
admin.site.register(Library)
admin.site.register(Permission)
admin.site.register(File)