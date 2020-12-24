# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/post/admin.py
# Compiled at: 2010-08-11 09:10:12
from django.contrib import admin
from panya.admin import ModelBaseAdmin
from post.models import Post
admin.site.register(Post, ModelBaseAdmin)