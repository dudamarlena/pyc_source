# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johsanca/Projects/luhu-blog-app/luhublog/context_processors.py
# Compiled at: 2015-10-20 16:35:47
from luhublog.models import Entry, Blog
BLOG = Blog.objects.get_blog()

def blog_info(request):
    return {'blog': BLOG}