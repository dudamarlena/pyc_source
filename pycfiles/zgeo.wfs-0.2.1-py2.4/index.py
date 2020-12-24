# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zgeo/wfs/geocatalog/index.py
# Compiled at: 2008-10-13 09:48:07
import os, persistent
from BTrees import IOBTree
from rtree import Rtree
try:
    import zope.app.appsetup.product as zap
    INDEX_DIR = zap.getProductConfiguration('zgeo.wfs')['directory']
except:
    INDEX_DIR = os.environ['CLIENT_HOME']

class BaseIndex(persistent.Persistent):
    __module__ = __name__

    def __init__(self):
        name = 'rtree-%s' % hash(repr(self))
        self._basepath = os.path.sep.join([INDEX_DIR, name])
        self.clear()

    def clear(self):
        self.backward = IOBTree.IOBTree()
        try:
            os.unlink('%s.dat' % self._basepath)
            os.unlink('%s.idx' % self._basepath)
        except:
            pass

    @property
    def rtree(self):
        return Rtree(self._basepath)