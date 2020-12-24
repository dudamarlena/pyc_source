# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/utils/admin.py
# Compiled at: 2015-08-17 17:37:49
from django.contrib import admin

class PictureInline(admin.TabularInline):
    template = 'meringue/edit_inline/gallery.html'
    extra = 0