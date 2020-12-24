# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/serialize/pickle.py
# Compiled at: 2012-05-23 13:18:32
from __future__ import unicode_literals, absolute_import
import pickle, cPickle
__all__ = [
 b'render_pickle', b'render_cpickle']

def render_pickle(data, template=None, i18n=None, **kw):
    """Serialize data using the Python pickle standard library.
    
    Accepts the same extended arguments as the pickle.dumps() function, see:
    
        http://www.python.org/doc/2.6/library/pickle.html#pickle.dumps
    
    """
    return (
     b'application/octet-stream', pickle.dumps(data, **kw))


def render_cpickle(data, template=None, i18n=None, **kw):
    """Serialize data using the Python cPickle standard library.
    
    Accepts the same extended arguments as the pickle.dumps() function, see:
    
        http://www.python.org/doc/2.6/library/pickle.html#pickle.dumps
    
    """
    return (
     b'application/octet-stream', cPickle.dumps(data, **kw))