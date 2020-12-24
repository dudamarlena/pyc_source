# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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