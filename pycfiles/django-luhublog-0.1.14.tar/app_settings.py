# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johsanca/Projects/luhu-blog-app/luhublog/app_settings.py
# Compiled at: 2015-10-20 16:35:47
from django.conf import settings
SEARCH_FIELDS = getattr(settings, 'BLOG_SEARCH_FIELDS', [
 'title', 'lead', 'content',
 'excerpt', 'image_caption', 'tags'])
TEST = 'esto es un test'