# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/nacl/partialfetcher.py
# Compiled at: 2007-12-02 16:26:59
from salamoia.h2o.object import *

class PartialFetcher(object):
    __module__ = __name__

    def __init__(self, controller, attributes):
        self.controller = controller
        self.attributes = attributes

    def __call__(self, id):
        obj = self.controller.baseFetch(id)
        partial = self.controller.defaultPartialObject()(obj, self.attributes)
        return partial


from salamoia.tests import *
runDocTests()