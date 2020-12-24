# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/serialize/pickle_.py
# Compiled at: 2010-03-18 05:47:02
import pickle, cPickle
__all__ = [
 'render_pickle', 'render_cpickle']

def render_pickle(data, template=None, **kw):
    """Serialize data using the Python pickle standard library.
    
    Accepts the same extended arguments as the pickle.dumps() function, see:
    
        http://www.python.org/doc/2.6/library/pickle.html#pickle.dumps
    
    """
    return (
     'application/octet-stream', pickle.dumps(data, **kw))


def render_cpickle(data, template=None, **kw):
    """Serialize data using the Python cPickle standard library.
    
    Accepts the same extended arguments as the pickle.dumps() function, see:
    
        http://www.python.org/doc/2.6/library/pickle.html#pickle.dumps
    
    """
    return (
     'application/octet-stream', cPickle.dumps(data, **kw))