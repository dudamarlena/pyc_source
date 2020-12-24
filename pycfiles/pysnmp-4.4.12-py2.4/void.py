# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/acmod/void.py
# Compiled at: 2019-08-18 17:24:05
from pysnmp.proto import errind, error
from pysnmp import debug

class Vacm(object):
    """Void Access Control Model"""
    __module__ = __name__
    accessModelID = 0

    def isAccessAllowed(self, snmpEngine, securityModel, securityName, securityLevel, viewType, contextName, variableName):
        debug.logger & debug.flagACL and debug.logger('isAccessAllowed: viewType %s for variableName %s - OK' % (viewType, variableName))
        return error.StatusInformation(errorIndication=errind.accessAllowed)