# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\__init__.py
# Compiled at: 2007-01-03 20:00:03
"""Template engine where Python is the template language."""
__author__ = 'L.C. Rees (lcrees-at-gmail.com)'
__revision__ = '0.5'
from webstring.xmlt import *
from webstring.html import *
from webstring.text import *

class Template(object):
    """Template dispatcher class."""
    __module__ = __name__

    def __new__(cls, *args, **kw):
        """Returns a template class."""
        format = kw.get('format', 'xml')
        if format == 'xml':
            return XMLTemplate(*args, **kw)
        elif format == 'html':
            return HTMLTemplate(*args, **kw)
        elif format == 'text':
            return TextTemplate(*args, **kw)