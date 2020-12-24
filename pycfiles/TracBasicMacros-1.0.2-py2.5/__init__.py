# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tracbmacros/__init__.py
# Compiled at: 2010-07-19 16:48:16
"""Simple but useful Trac macros

Expand Trac capabilities by embed simple snippets in wiki pages using simple macros.

Copyright 2009-2011 Olemis Lang <olemis at gmail.com>
Licensed under the Apache License
"""
__author__ = 'Olemis Lang'
from trac.core import TracError
TracError.__str__ = lambda self: unicode(self).encode('ascii', 'ignore')
try:
    from tracbmacros.config import *
    from tracbmacros.wiki import *
    msg = 'Ok'
except Exception, exc:
    msg = "Exception %s raised: '%s'" % (exc.__class__.__name__, str(exc))