# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./CosPersistencePDS_idl.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 3979 bytes
import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA
_omnipy.checkVersion(4, 2, __file__, 1)
try:
    property
except NameError:

    def property(*args):
        pass


import CosPersistencePID_idl
_0_CosPersistencePID = omniORB.openModule('CosPersistencePID')
_0_CosPersistencePID__POA = omniORB.openModule('CosPersistencePID__POA')
__name__ = 'CosPersistencePDS'
_0_CosPersistencePDS = omniORB.openModule('CosPersistencePDS', '/tmp/corba/omni/share/idl/omniORB/COS/CosPersistencePDS.idl')
_0_CosPersistencePDS__POA = omniORB.openModule('CosPersistencePDS__POA', '/tmp/corba/omni/share/idl/omniORB/COS/CosPersistencePDS.idl')
_0_CosPersistencePDS._d_PDS = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosPersistencePDS/PDS:1.0', 'PDS')
omniORB.typeMapping['IDL:omg.org/CosPersistencePDS/PDS:1.0'] = _0_CosPersistencePDS._d_PDS
_0_CosPersistencePDS.PDS = omniORB.newEmptyClass()

class PDS:
    _NP_RepositoryId = _0_CosPersistencePDS._d_PDS[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosPersistencePDS.PDS = PDS
_0_CosPersistencePDS._tc_PDS = omniORB.tcInternal.createTypeCode(_0_CosPersistencePDS._d_PDS)
omniORB.registerType(PDS._NP_RepositoryId, _0_CosPersistencePDS._d_PDS, _0_CosPersistencePDS._tc_PDS)
PDS._d_connect = (
 (
  omniORB.typeMapping['IDL:omg.org/CORBA/Object:1.0'], omniORB.typeMapping['IDL:omg.org/CosPersistencePID/PID:1.0']), (omniORB.typeMapping['IDL:omg.org/CosPersistencePDS/PDS:1.0'],), None)
PDS._d_disconnect = ((omniORB.typeMapping['IDL:omg.org/CORBA/Object:1.0'], omniORB.typeMapping['IDL:omg.org/CosPersistencePID/PID:1.0']), (), None)
PDS._d_store = ((omniORB.typeMapping['IDL:omg.org/CORBA/Object:1.0'], omniORB.typeMapping['IDL:omg.org/CosPersistencePID/PID:1.0']), (), None)
PDS._d_restore = ((omniORB.typeMapping['IDL:omg.org/CORBA/Object:1.0'], omniORB.typeMapping['IDL:omg.org/CosPersistencePID/PID:1.0']), (), None)
PDS._d_delete = ((omniORB.typeMapping['IDL:omg.org/CORBA/Object:1.0'], omniORB.typeMapping['IDL:omg.org/CosPersistencePID/PID:1.0']), (), None)

class _objref_PDS(CORBA.Object):
    _NP_RepositoryId = PDS._NP_RepositoryId

    def __init__(self, obj):
        CORBA.Object.__init__(self, obj)

    def connect(self, *args):
        return self._obj.invoke('connect', _0_CosPersistencePDS.PDS._d_connect, args)

    def disconnect(self, *args):
        return self._obj.invoke('disconnect', _0_CosPersistencePDS.PDS._d_disconnect, args)

    def store(self, *args):
        return self._obj.invoke('store', _0_CosPersistencePDS.PDS._d_store, args)

    def restore(self, *args):
        return self._obj.invoke('restore', _0_CosPersistencePDS.PDS._d_restore, args)

    def delete(self, *args):
        return self._obj.invoke('delete', _0_CosPersistencePDS.PDS._d_delete, args)


omniORB.registerObjref(PDS._NP_RepositoryId, _objref_PDS)
_0_CosPersistencePDS._objref_PDS = _objref_PDS
del PDS
del _objref_PDS
__name__ = 'CosPersistencePDS__POA'

class PDS(PortableServer.Servant):
    _NP_RepositoryId = _0_CosPersistencePDS.PDS._NP_RepositoryId
    _omni_op_d = {'connect':_0_CosPersistencePDS.PDS._d_connect, 
     'disconnect':_0_CosPersistencePDS.PDS._d_disconnect,  'store':_0_CosPersistencePDS.PDS._d_store,  'restore':_0_CosPersistencePDS.PDS._d_restore,  'delete':_0_CosPersistencePDS.PDS._d_delete}


PDS._omni_skeleton = PDS
_0_CosPersistencePDS__POA.PDS = PDS
omniORB.registerSkeleton(PDS._NP_RepositoryId, PDS)
del PDS
__name__ = 'CosPersistencePDS'
__name__ = 'CosPersistencePDS_idl'
_exported_modules = ('CosPersistencePDS', )