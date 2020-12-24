# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydo/guesscache.py
# Compiled at: 2007-02-15 13:23:36
import cPickle, os, tempfile, time
from pydo.utils import getuser

class GuessCache(object):
    """
    a cache that stores pickles of data associated with a Python class.
    """
    __module__ = __name__

    def __init__(self, cachedir=None):
        if cachedir is None:
            cachedir = os.path.join(tempfile.gettempdir(), ('_').join((x for x in (getuser(), 'pydoguesscache') if x)))
        self.cachedir = cachedir
        if os.path.exists(cachedir):
            if not os.path.isdir(cachedir):
                raise RuntimeException, 'not a directory: %s' % cachedir
            if not os.access(cachedir, os.W_OK | os.R_OK | os.X_OK):
                raise RuntimeException, 'cannot access directory: %s' % cachedir
        else:
            os.makedirs(cachedir)
        return

    def pathForObj(self, obj, make=False):
        pathElems = [self.cachedir] + obj.__module__.split('.')
        path = os.path.join(*pathElems)
        if make:
            if not os.path.exists(path):
                os.makedirs(path)
        return os.path.join(path, '%s.cache' % obj.__name__)

    def retrieve(self, obj):
        path = self.pathForObj(obj)
        if os.path.exists(path):
            fp = open(path, 'rb')
            data = cPickle.load(fp)
            fp.close()
            return data
        return

    def clear(self, obj):
        path = self.pathForObj(obj)
        if os.path.exists(path):
            os.remove(path)

    def store(self, obj, data):
        path = self.pathForObj(obj, True)
        tmppath = '%s~%d%d' % (path, os.getpid(), int(time.time()))
        fp = open(tmppath, 'wb')
        cPickle.dump(data, fp, 2)
        fp.close()
        os.rename(tmppath, path)


__all__ = [
 'GuessCache']