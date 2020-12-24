# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/urlimport/__init__.py
# Compiled at: 2010-04-16 12:46:44
"""enables to import modules through the web, by adding urls to the python path.
"""
import sys
from urlimport import UrlFinder, config, reset, DefaultErrorHandler
__all__ = ('config', 'reset', 'DefaultErrorHandler')
sys.path_hooks = [ x for x in sys.path_hooks if x.__name__ != 'UrlFinder' ] + [UrlFinder]