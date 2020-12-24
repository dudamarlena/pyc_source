# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/management/interfacemgr/Interface.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 659 bytes
""" Class description goes here. """
from dataclay.util.MgrObject import ManagementObject

class Interface(ManagementObject):
    _fields = [
     'dataClayID',
     'providerAccountName',
     'namespace',
     'classNamespace',
     'className',
     'propertiesInIface',
     'operationsSignatureInIface']
    _internal_fields = [
     'providerAccountID',
     'namespaceID',
     'classNamespaceID',
     'metaClassID',
     'operationsIDs',
     'propertiesIDs']