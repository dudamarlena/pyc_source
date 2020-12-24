# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vellum/settings.py
# Compiled at: 2012-09-16 02:10:18
"""
These blog settings should not be edited directly.
Instead, overwrite them in the main project's setting file.
"""
from django.conf import settings
from django.contrib.sites.models import Site
BLOG_NAME = getattr(settings, 'BLOG_NAME', Site.objects.get_current().name)
BLOG_DESCRIPTION = getattr(settings, 'BLOG_DESCRIPTION', 'A basic Django blog')
BLOG_PAGESIZE = getattr(settings, 'BLOG_PAGESIZE', 12)
BLOG_FEEDSIZE = getattr(settings, 'BLOG_FEEDSIZE', BLOG_PAGESIZE)
BLOG_EXCERPTLENGTH = getattr(settings, 'BLOG_EXCERPTLENGTH', 100)
BLOG_WMD = getattr(settings, 'BLOG_WMD', False)
BLOG_INTERNALIPS = getattr(settings, 'BLOG_INTERNALIPS', settings.INTERNAL_IPS)
BLOG_USEDISQUS = getattr(settings, 'BLOG_USEDISQUS', False)
try:
    import smartypants
    smartyimport = True
except ImportError:
    smartyimport = False

BLOG_SMARTYPANTS = getattr(settings, 'BLOG_SMARTYPANTS', smartyimport)