# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/serialize/marshal.py
# Compiled at: 2012-05-23 13:18:32
from __future__ import unicode_literals, absolute_import
import marshal
__all__ = [
 b'render']

def render(data, template=None, i18n=None, **kw):
    """Serialize data using Python marshal standard library.
    
    Accepts the same extended arguments as the marshal.dumps() function, see:
    
        http://www.python.org/doc/2.6/library/marshal.html#marshal.dumps
    
    """
    return (
     b'application/octet-stream', marshal.dumps(data, **kw))