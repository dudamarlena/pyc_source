# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/management/classmgr/Implementation.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 776 bytes
""" Class description goes here. """
from dataclay.util.MgrObject import ManagementObject

class Implementation(ManagementObject):
    _fields = [
     'dataClayID',
     'responsibleAccountName',
     'namespace',
     'className',
     'opNameAndDescriptor',
     'position',
     'includes',
     'accessedProperties',
     'accessedImplementations',
     'requiredQuantitativeFeatures',
     'requiredQualitativeFeatures']
    _internal_fields = [
     'operationID',
     'metaClassID',
     'responsibleAccountID',
     'namespaceID',
     'prefetchingInfo']