# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: routines.py
# Compiled at: 2017-09-06 23:21:49
from aclpagerank import aclpagerank
from aclpagerank_weighted import aclpagerank_weighted
from list_to_CSR import list_to_CSR
from MQI import MQI
from ppr_path import ppr_path
from proxl1PRaccel import proxl1PRaccel
from sweepcut import sweepcut

class GRAPH(object):

    def list_to_CSR(self, filename):
        return list_to_CSR(filename)

    def aclpagerank():
        aclpagerank

    aclpagerank_weighted = aclpagerank_weighted
    MQI = MQI
    ppr_path = ppr_path
    proxl1PRaccel = proxl1PRaccel
    sweepcut = sweepcut