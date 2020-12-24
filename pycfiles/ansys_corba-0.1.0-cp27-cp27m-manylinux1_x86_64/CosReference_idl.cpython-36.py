# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./CosReference_idl.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 6963 bytes
import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA
_omnipy.checkVersion(4, 2, __file__, 1)
try:
    property
except NameError:

    def property(*args):
        pass


import corbaidl_idl
_0_CORBA = omniORB.openModule('CORBA')
_0_CORBA__POA = omniORB.openModule('CORBA__POA')
import boxes_idl
_0_CORBA = omniORB.openModule('CORBA')
_0_CORBA__POA = omniORB.openModule('CORBA__POA')
import ir_idl
_0_CORBA = omniORB.openModule('CORBA')
_0_CORBA__POA = omniORB.openModule('CORBA__POA')
import CosObjectIdentity_idl
_0_CosObjectIdentity = omniORB.openModule('CosObjectIdentity')
_0_CosObjectIdentity__POA = omniORB.openModule('CosObjectIdentity__POA')
import CosRelationships_idl
_0_CosRelationships = omniORB.openModule('CosRelationships')
_0_CosRelationships__POA = omniORB.openModule('CosRelationships__POA')
import CosGraphs_idl
_0_CosGraphs = omniORB.openModule('CosGraphs')
_0_CosGraphs__POA = omniORB.openModule('CosGraphs__POA')
__name__ = 'CosReference'
_0_CosReference = omniORB.openModule('CosReference', '/tmp/corba/omni/share/idl/omniORB/COS/CosReference.idl')
_0_CosReference__POA = omniORB.openModule('CosReference__POA', '/tmp/corba/omni/share/idl/omniORB/COS/CosReference.idl')
_0_CosReference._d_Relationship = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosReference/Relationship:1.0', 'Relationship')
omniORB.typeMapping['IDL:omg.org/CosReference/Relationship:1.0'] = _0_CosReference._d_Relationship
_0_CosReference.Relationship = omniORB.newEmptyClass()

class Relationship(_0_CosRelationships.Relationship):
    _NP_RepositoryId = _0_CosReference._d_Relationship[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosReference.Relationship = Relationship
_0_CosReference._tc_Relationship = omniORB.tcInternal.createTypeCode(_0_CosReference._d_Relationship)
omniORB.registerType(Relationship._NP_RepositoryId, _0_CosReference._d_Relationship, _0_CosReference._tc_Relationship)

class _objref_Relationship(_0_CosRelationships._objref_Relationship):
    _NP_RepositoryId = Relationship._NP_RepositoryId

    def __init__(self, obj):
        _0_CosRelationships._objref_Relationship.__init__(self, obj)


omniORB.registerObjref(Relationship._NP_RepositoryId, _objref_Relationship)
_0_CosReference._objref_Relationship = _objref_Relationship
del Relationship
del _objref_Relationship
__name__ = 'CosReference__POA'

class Relationship(_0_CosRelationships__POA.Relationship):
    _NP_RepositoryId = _0_CosReference.Relationship._NP_RepositoryId
    _omni_op_d = {}
    _omni_op_d.update(_0_CosRelationships__POA.Relationship._omni_op_d)


Relationship._omni_skeleton = Relationship
_0_CosReference__POA.Relationship = Relationship
omniORB.registerSkeleton(Relationship._NP_RepositoryId, Relationship)
del Relationship
__name__ = 'CosReference'
_0_CosReference._d_ReferencesRole = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosReference/ReferencesRole:1.0', 'ReferencesRole')
omniORB.typeMapping['IDL:omg.org/CosReference/ReferencesRole:1.0'] = _0_CosReference._d_ReferencesRole
_0_CosReference.ReferencesRole = omniORB.newEmptyClass()

class ReferencesRole(_0_CosGraphs.Role):
    _NP_RepositoryId = _0_CosReference._d_ReferencesRole[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosReference.ReferencesRole = ReferencesRole
_0_CosReference._tc_ReferencesRole = omniORB.tcInternal.createTypeCode(_0_CosReference._d_ReferencesRole)
omniORB.registerType(ReferencesRole._NP_RepositoryId, _0_CosReference._d_ReferencesRole, _0_CosReference._tc_ReferencesRole)

class _objref_ReferencesRole(_0_CosGraphs._objref_Role):
    _NP_RepositoryId = ReferencesRole._NP_RepositoryId

    def __init__(self, obj):
        _0_CosGraphs._objref_Role.__init__(self, obj)


omniORB.registerObjref(ReferencesRole._NP_RepositoryId, _objref_ReferencesRole)
_0_CosReference._objref_ReferencesRole = _objref_ReferencesRole
del ReferencesRole
del _objref_ReferencesRole
__name__ = 'CosReference__POA'

class ReferencesRole(_0_CosGraphs__POA.Role):
    _NP_RepositoryId = _0_CosReference.ReferencesRole._NP_RepositoryId
    _omni_op_d = {}
    _omni_op_d.update(_0_CosGraphs__POA.Role._omni_op_d)


ReferencesRole._omni_skeleton = ReferencesRole
_0_CosReference__POA.ReferencesRole = ReferencesRole
omniORB.registerSkeleton(ReferencesRole._NP_RepositoryId, ReferencesRole)
del ReferencesRole
__name__ = 'CosReference'
_0_CosReference._d_ReferencedByRole = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosReference/ReferencedByRole:1.0', 'ReferencedByRole')
omniORB.typeMapping['IDL:omg.org/CosReference/ReferencedByRole:1.0'] = _0_CosReference._d_ReferencedByRole
_0_CosReference.ReferencedByRole = omniORB.newEmptyClass()

class ReferencedByRole(_0_CosGraphs.Role):
    _NP_RepositoryId = _0_CosReference._d_ReferencedByRole[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosReference.ReferencedByRole = ReferencedByRole
_0_CosReference._tc_ReferencedByRole = omniORB.tcInternal.createTypeCode(_0_CosReference._d_ReferencedByRole)
omniORB.registerType(ReferencedByRole._NP_RepositoryId, _0_CosReference._d_ReferencedByRole, _0_CosReference._tc_ReferencedByRole)

class _objref_ReferencedByRole(_0_CosGraphs._objref_Role):
    _NP_RepositoryId = ReferencedByRole._NP_RepositoryId

    def __init__(self, obj):
        _0_CosGraphs._objref_Role.__init__(self, obj)


omniORB.registerObjref(ReferencedByRole._NP_RepositoryId, _objref_ReferencedByRole)
_0_CosReference._objref_ReferencedByRole = _objref_ReferencedByRole
del ReferencedByRole
del _objref_ReferencedByRole
__name__ = 'CosReference__POA'

class ReferencedByRole(_0_CosGraphs__POA.Role):
    _NP_RepositoryId = _0_CosReference.ReferencedByRole._NP_RepositoryId
    _omni_op_d = {}
    _omni_op_d.update(_0_CosGraphs__POA.Role._omni_op_d)


ReferencedByRole._omni_skeleton = ReferencedByRole
_0_CosReference__POA.ReferencedByRole = ReferencedByRole
omniORB.registerSkeleton(ReferencedByRole._NP_RepositoryId, ReferencedByRole)
del ReferencedByRole
__name__ = 'CosReference'
__name__ = 'CosReference_idl'
_exported_modules = ('CosReference', )