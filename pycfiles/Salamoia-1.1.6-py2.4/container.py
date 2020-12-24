# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/container.py
# Compiled at: 2007-12-02 16:26:58
from salamoia.h2o.object import Object

class ObjectContainer(Object):
    """
    This object is used to contain objects that are not
    subclasses of h2o.Object because you may not transfer them
    through the xmlrpc connection without Object magic....
    For example you can not transfer a list of Object-s but
    you must wrap a Container around the list because the root of
    the graph must be a subclass of Object (TODO: fix that)

    OBSOLETE
    """
    __module__ = __name__

    def __init__(self, value):
        Object.__init__(self, '')
        self.value = value

    def resurrect(self):
        return self.value


Container = ObjectContainer
from salamoia.tests import *
runDocTests()