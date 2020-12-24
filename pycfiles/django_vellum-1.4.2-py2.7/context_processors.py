# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vellum/context_processors.py
# Compiled at: 2012-09-16 02:10:18
from vellum import settings

def blog_settings(request):
    """
    Add blog settings to the context, making them available to templates.
    """
    return {'BLOG_NAME': settings.BLOG_NAME, 
       'BLOG_DESCRIPTION': settings.BLOG_DESCRIPTION, 
       'BLOG_EXCERPTLENGTH': settings.BLOG_EXCERPTLENGTH, 
       'BLOG_USEDISQUS': settings.BLOG_USEDISQUS}