# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/util/threadinglocal.py
# Compiled at: 2012-02-27 07:41:58
"""
Implementation of thread-local storage, for Python versions that don't
have thread local storage natively.
"""
try:
    import threading
except ImportError:

    class local(object):
        pass


else:
    try:
        local = threading.local
    except AttributeError:
        import thread

        class local(object):

            def __init__(self):
                self.__dict__['__objs'] = {}

            def __getattr__(self, attr, g=thread.get_ident):
                try:
                    return self.__dict__['__objs'][g()][attr]
                except KeyError:
                    raise AttributeError('No variable %s defined for the thread %s' % (
                     attr, g()))

            def __setattr__(self, attr, value, g=thread.get_ident):
                self.__dict__['__objs'].setdefault(g(), {})[attr] = value

            def __delattr__(self, attr, g=thread.get_ident):
                try:
                    del self.__dict__['__objs'][g()][attr]
                except KeyError:
                    raise AttributeError('No variable %s defined for thread %s' % (
                     attr, g()))