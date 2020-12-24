# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/servers/tools/boutils.py
# Compiled at: 2008-10-01 10:39:52
from xooof.xmldispatcher.interfaces.interfaces import *
from xooof.xmlstruct.xmlstruct import XMLStructError

def validateRqst(rqst, baseClass, canBeNull=0, mustBeValidated=1):
    if rqst is None:
        if not canBeNull:
            raise XMLDispatcherUserException('Missing rqst', code='XDE_VAL_RQST_MISSING')
    else:
        if not isinstance(rqst, baseClass):
            raise XMLDispatcherUserException('Unexpected rqst type (got %s, expecting %s)' % (type(rqst), baseClass), code='XDE_VAL_RQST_INV_TYPE')
        if mustBeValidated:
            try:
                rqst.xsValidate('rqst')
            except XMLStructError, e:
                raise XMLDispatcherUserException(str(e), code='XDE_VAL_RQST_INV')

    return


def validateRply(rply, baseClass, canBeNull=0, mustBeValidated=1):
    if rply is None:
        if not canBeNull:
            raise XMLDispatcherAppException('Missing rply', code='XDE_VAL_RPLY_MISSING')
    else:
        if not isinstance(rply, baseClass):
            raise XMLDispatcherAppException('Unexpected rply type (got %s, expecting %s)' % (type(rply), baseClass), code='XDE_VAL_RPLY_INV_TYPE')
        if mustBeValidated:
            try:
                rply.xsValidate('rply')
            except XMLStructError, e:
                raise XMLDispatcherAppException(str(e), code='XDE_VAL_RPLY_INV')

    return