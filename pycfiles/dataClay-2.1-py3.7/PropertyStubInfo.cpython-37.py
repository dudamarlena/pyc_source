# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/management/stubs/PropertyStubInfo.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 592 bytes
""" Class description goes here. """
from dataclay.util.MgrObject import ManagementObject
import dataclay.util.management.classmgr.Type as Type

class PropertyStubInfo(ManagementObject):
    _fields = [
     'namespace',
     'propertyName',
     'namespaceID',
     'propertyID',
     'propertyType',
     'getterOperationID',
     'setterOperationID',
     'beforeUpdate',
     'afterUpdate',
     'inMaster']
    _internal_fields = list()
    _typed_fields = {'propertyType': Type}