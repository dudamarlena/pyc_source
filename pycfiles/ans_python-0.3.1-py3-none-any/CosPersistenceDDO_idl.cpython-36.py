# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./CosPersistenceDDO_idl.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 6025 bytes
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
__name__ = 'CosPersistenceDDO'
_0_CosPersistenceDDO = omniORB.openModule('CosPersistenceDDO', '/tmp/corba/omni/share/idl/omniORB/COS/CosPersistenceDDO.idl')
_0_CosPersistenceDDO__POA = omniORB.openModule('CosPersistenceDDO__POA', '/tmp/corba/omni/share/idl/omniORB/COS/CosPersistenceDDO.idl')
_0_CosPersistenceDDO._d_DDO = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosPersistenceDDO/DDO:1.0', 'DDO')
omniORB.typeMapping['IDL:omg.org/CosPersistenceDDO/DDO:1.0'] = _0_CosPersistenceDDO._d_DDO
_0_CosPersistenceDDO.DDO = omniORB.newEmptyClass()

class DDO:
    _NP_RepositoryId = _0_CosPersistenceDDO._d_DDO[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosPersistenceDDO.DDO = DDO
_0_CosPersistenceDDO._tc_DDO = omniORB.tcInternal.createTypeCode(_0_CosPersistenceDDO._d_DDO)
omniORB.registerType(DDO._NP_RepositoryId, _0_CosPersistenceDDO._d_DDO, _0_CosPersistenceDDO._tc_DDO)
DDO._d__get_object_type = ((), ((omniORB.tcInternal.tv_string, 0),), None)
DDO._d__set_object_type = (
 (
  (
   omniORB.tcInternal.tv_string, 0),), (), None)
DDO._d__get_p = ((), (omniORB.typeMapping['IDL:omg.org/CosPersistencePID/PID:1.0'],), None)
DDO._d__set_p = ((omniORB.typeMapping['IDL:omg.org/CosPersistencePID/PID:1.0'],), (), None)
DDO._d_add_data = ((), (omniORB.tcInternal.tv_short,), None)
DDO._d_add_data_property = ((omniORB.tcInternal.tv_short,), (omniORB.tcInternal.tv_short,), None)
DDO._d_get_data_count = ((), (omniORB.tcInternal.tv_short,), None)
DDO._d_get_data_property_count = ((omniORB.tcInternal.tv_short,), (omniORB.tcInternal.tv_short,), None)
DDO._d_get_data_property = ((omniORB.tcInternal.tv_short, omniORB.tcInternal.tv_short), ((omniORB.tcInternal.tv_string, 0), omniORB.tcInternal.tv_any), None)
DDO._d_set_data_property = ((omniORB.tcInternal.tv_short, omniORB.tcInternal.tv_short, (omniORB.tcInternal.tv_string, 0), omniORB.tcInternal.tv_any), (), None)
DDO._d_get_data = ((omniORB.tcInternal.tv_short,), ((omniORB.tcInternal.tv_string, 0), omniORB.tcInternal.tv_any), None)
DDO._d_set_data = ((omniORB.tcInternal.tv_short, (omniORB.tcInternal.tv_string, 0), omniORB.tcInternal.tv_any), (), None)

class _objref_DDO(CORBA.Object):
    _NP_RepositoryId = DDO._NP_RepositoryId

    def __init__(self, obj):
        CORBA.Object.__init__(self, obj)

    def _get_object_type(self, *args):
        return self._obj.invoke('_get_object_type', _0_CosPersistenceDDO.DDO._d__get_object_type, args)

    def _set_object_type(self, *args):
        return self._obj.invoke('_set_object_type', _0_CosPersistenceDDO.DDO._d__set_object_type, args)

    object_type = property(_get_object_type, _set_object_type)

    def _get_p(self, *args):
        return self._obj.invoke('_get_p', _0_CosPersistenceDDO.DDO._d__get_p, args)

    def _set_p(self, *args):
        return self._obj.invoke('_set_p', _0_CosPersistenceDDO.DDO._d__set_p, args)

    p = property(_get_p, _set_p)

    def add_data(self, *args):
        return self._obj.invoke('add_data', _0_CosPersistenceDDO.DDO._d_add_data, args)

    def add_data_property(self, *args):
        return self._obj.invoke('add_data_property', _0_CosPersistenceDDO.DDO._d_add_data_property, args)

    def get_data_count(self, *args):
        return self._obj.invoke('get_data_count', _0_CosPersistenceDDO.DDO._d_get_data_count, args)

    def get_data_property_count(self, *args):
        return self._obj.invoke('get_data_property_count', _0_CosPersistenceDDO.DDO._d_get_data_property_count, args)

    def get_data_property(self, *args):
        return self._obj.invoke('get_data_property', _0_CosPersistenceDDO.DDO._d_get_data_property, args)

    def set_data_property(self, *args):
        return self._obj.invoke('set_data_property', _0_CosPersistenceDDO.DDO._d_set_data_property, args)

    def get_data(self, *args):
        return self._obj.invoke('get_data', _0_CosPersistenceDDO.DDO._d_get_data, args)

    def set_data(self, *args):
        return self._obj.invoke('set_data', _0_CosPersistenceDDO.DDO._d_set_data, args)


omniORB.registerObjref(DDO._NP_RepositoryId, _objref_DDO)
_0_CosPersistenceDDO._objref_DDO = _objref_DDO
del DDO
del _objref_DDO
__name__ = 'CosPersistenceDDO__POA'

class DDO(PortableServer.Servant):
    _NP_RepositoryId = _0_CosPersistenceDDO.DDO._NP_RepositoryId
    _omni_op_d = {'_get_object_type':_0_CosPersistenceDDO.DDO._d__get_object_type, 
     '_set_object_type':_0_CosPersistenceDDO.DDO._d__set_object_type,  '_get_p':_0_CosPersistenceDDO.DDO._d__get_p,  '_set_p':_0_CosPersistenceDDO.DDO._d__set_p,  'add_data':_0_CosPersistenceDDO.DDO._d_add_data,  'add_data_property':_0_CosPersistenceDDO.DDO._d_add_data_property,  'get_data_count':_0_CosPersistenceDDO.DDO._d_get_data_count,  'get_data_property_count':_0_CosPersistenceDDO.DDO._d_get_data_property_count,  'get_data_property':_0_CosPersistenceDDO.DDO._d_get_data_property,  'set_data_property':_0_CosPersistenceDDO.DDO._d_set_data_property,  'get_data':_0_CosPersistenceDDO.DDO._d_get_data,  'set_data':_0_CosPersistenceDDO.DDO._d_set_data}


DDO._omni_skeleton = DDO
_0_CosPersistenceDDO__POA.DDO = DDO
omniORB.registerSkeleton(DDO._NP_RepositoryId, DDO)
del DDO
__name__ = 'CosPersistenceDDO'
__name__ = 'CosPersistenceDDO_idl'
_exported_modules = ('CosPersistenceDDO', )