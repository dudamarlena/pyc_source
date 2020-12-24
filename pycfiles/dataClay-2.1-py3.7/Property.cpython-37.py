# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/management/classmgr/Property.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 1004 bytes
""" Class description goes here. """
from dataclay.util.MgrObject import ManagementObject
from .Type import Type

class Property(ManagementObject):
    _fields = [
     'dataClayID',
     'namespace',
     'className',
     'name',
     'position',
     'type']
    _internal_fields = [
     'getterOperationID',
     'getterImplementationID',
     'setterImplementationID',
     'setterOperationID',
     'updateOperationID',
     'updateImplementationID',
     'inMaster',
     'beforeUpdate',
     'afterUpdate',
     'namespaceID',
     'metaClassID',
     'languageDepInfos',
     'annotations']
    _typed_fields = {'type': Type}