# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid_move/rain/move/EucaService.py
# Compiled at: 2012-06-20 12:31:45
from futuregrid_move.rain.move.Resource import Resource, Node, Cluster, Service

class EucaService(Service):

    def __init__(self, resId, res=dict()):
        super(EucaService, self).__init__()
        self._id = resId
        self._type = 'Eucalyptus'
        self._res = res

    def cbadd(self, ares):
        print 'INSIDE EucaService:cbadd: Added ' + ares.identifier + ' to service ' + self.identifier

    def cbremove(self, ares):
        print 'INSIDE EucaService:cbremove: Removed ' + ares.identifier + ' from service ' + self.identifier