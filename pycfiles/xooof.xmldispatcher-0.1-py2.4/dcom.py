# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/clients/adapters/dcom.py
# Compiled at: 2008-10-01 10:39:43
import warnings
from win32com.client import DispatchEx, CastTo
import pythoncom
from com import COMAdapter

def _CreateObject(progId, machine=None):
    try:
        o = DispatchEx(progId, machine)
        try:
            return CastTo(o, 'IXMLDispatcher')
        except:
            warnings.warn('%s@%s does not support the IXMLDispatcher interface, trying with default interface' % (progId, machine))
            return o

    except pythoncom.com_error, errorData:
        raise RuntimeError, 'CreateObject(%s,%s) failed: %s' % (progId, machine, errorData)


class DCOMAdapter(COMAdapter):
    __module__ = __name__

    def __init__(self, appName, hostName=None, componentName='XMLDispatcher'):
        COMAdapter.__init__(self)
        self.__appName = appName
        self.__hostName = hostName
        self.__componentName = componentName

    def _connect(self):
        return _CreateObject(self.__appName + '.' + self.__componentName, self.__hostName)