# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/serialize/marshal_.py
# Compiled at: 2010-03-18 05:47:02
import marshal
__all__ = [
 'render']

def render(data, template=None, **kw):
    """Serialize data using Python marshal standard library.
    
    Accepts the same extended arguments as the marshal.dumps() function, see:
    
        http://www.python.org/doc/2.6/library/marshal.html#marshal.dumps
    
    """
    return (
     'application/octet-stream', marshal.dumps(data, **kw))