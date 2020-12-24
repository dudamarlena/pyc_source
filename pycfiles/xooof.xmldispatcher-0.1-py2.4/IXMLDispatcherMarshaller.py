# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/tools/marshallers/IXMLDispatcherMarshaller.py
# Compiled at: 2008-10-01 10:39:37


class IXMLDispatcherMarshaller:
    __module__ = __name__

    def marshall(self, o):
        """Marshal the python object and return a string"""
        pass

    def marshallId(self, instanceId):
        """Marshal the instanceId string and return a string"""
        pass

    def unmarshall(self, s):
        """Unmarshal the string and return a python object """
        pass

    def unmarshallId(self, s):
        """Unmarshal the string and return an instanceId string """
        pass