# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./CosTradingDynamic_idl.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 5508 bytes
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
import CosTrading_idl
_0_CosTrading = omniORB.openModule('CosTrading')
_0_CosTrading__POA = omniORB.openModule('CosTrading__POA')
__name__ = 'CosTradingDynamic'
_0_CosTradingDynamic = omniORB.openModule('CosTradingDynamic', '/tmp/corba/omni/share/idl/omniORB/COS/CosTradingDynamic.idl')
_0_CosTradingDynamic__POA = omniORB.openModule('CosTradingDynamic__POA', '/tmp/corba/omni/share/idl/omniORB/COS/CosTradingDynamic.idl')
_0_CosTradingDynamic.DPEvalFailure = omniORB.newEmptyClass()

class DPEvalFailure(CORBA.UserException):
    _NP_RepositoryId = 'IDL:omg.org/CosTradingDynamic/DPEvalFailure:1.0'

    def __init__(self, name, returned_type, extra_info):
        CORBA.UserException.__init__(self, name, returned_type, extra_info)
        self.name = name
        self.returned_type = returned_type
        self.extra_info = extra_info


_0_CosTradingDynamic.DPEvalFailure = DPEvalFailure
_0_CosTradingDynamic._d_DPEvalFailure = (omniORB.tcInternal.tv_except, DPEvalFailure, DPEvalFailure._NP_RepositoryId, 'DPEvalFailure', 'name', omniORB.typeMapping['IDL:omg.org/CosTrading/PropertyName:1.0'], 'returned_type', omniORB.tcInternal.tv_TypeCode, 'extra_info', omniORB.tcInternal.tv_any)
_0_CosTradingDynamic._tc_DPEvalFailure = omniORB.tcInternal.createTypeCode(_0_CosTradingDynamic._d_DPEvalFailure)
omniORB.registerType(DPEvalFailure._NP_RepositoryId, _0_CosTradingDynamic._d_DPEvalFailure, _0_CosTradingDynamic._tc_DPEvalFailure)
del DPEvalFailure
_0_CosTradingDynamic._d_DynamicPropEval = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosTradingDynamic/DynamicPropEval:1.0', 'DynamicPropEval')
omniORB.typeMapping['IDL:omg.org/CosTradingDynamic/DynamicPropEval:1.0'] = _0_CosTradingDynamic._d_DynamicPropEval
_0_CosTradingDynamic.DynamicPropEval = omniORB.newEmptyClass()

class DynamicPropEval:
    _NP_RepositoryId = _0_CosTradingDynamic._d_DynamicPropEval[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosTradingDynamic.DynamicPropEval = DynamicPropEval
_0_CosTradingDynamic._tc_DynamicPropEval = omniORB.tcInternal.createTypeCode(_0_CosTradingDynamic._d_DynamicPropEval)
omniORB.registerType(DynamicPropEval._NP_RepositoryId, _0_CosTradingDynamic._d_DynamicPropEval, _0_CosTradingDynamic._tc_DynamicPropEval)
DynamicPropEval._d_evalDP = (
 (
  omniORB.typeMapping['IDL:omg.org/CosTrading/PropertyName:1.0'], omniORB.tcInternal.tv_TypeCode, omniORB.tcInternal.tv_any), (omniORB.tcInternal.tv_any,), {_0_CosTradingDynamic.DPEvalFailure._NP_RepositoryId: _0_CosTradingDynamic._d_DPEvalFailure})

class _objref_DynamicPropEval(CORBA.Object):
    _NP_RepositoryId = DynamicPropEval._NP_RepositoryId

    def __init__(self, obj):
        CORBA.Object.__init__(self, obj)

    def evalDP(self, *args):
        return self._obj.invoke('evalDP', _0_CosTradingDynamic.DynamicPropEval._d_evalDP, args)


omniORB.registerObjref(DynamicPropEval._NP_RepositoryId, _objref_DynamicPropEval)
_0_CosTradingDynamic._objref_DynamicPropEval = _objref_DynamicPropEval
del DynamicPropEval
del _objref_DynamicPropEval
__name__ = 'CosTradingDynamic__POA'

class DynamicPropEval(PortableServer.Servant):
    _NP_RepositoryId = _0_CosTradingDynamic.DynamicPropEval._NP_RepositoryId
    _omni_op_d = {'evalDP': _0_CosTradingDynamic.DynamicPropEval._d_evalDP}


DynamicPropEval._omni_skeleton = DynamicPropEval
_0_CosTradingDynamic__POA.DynamicPropEval = DynamicPropEval
omniORB.registerSkeleton(DynamicPropEval._NP_RepositoryId, DynamicPropEval)
del DynamicPropEval
__name__ = 'CosTradingDynamic'
_0_CosTradingDynamic.DynamicProp = omniORB.newEmptyClass()

class DynamicProp(omniORB.StructBase):
    _NP_RepositoryId = 'IDL:omg.org/CosTradingDynamic/DynamicProp:1.0'

    def __init__(self, eval_if, returned_type, extra_info):
        self.eval_if = eval_if
        self.returned_type = returned_type
        self.extra_info = extra_info


_0_CosTradingDynamic.DynamicProp = DynamicProp
_0_CosTradingDynamic._d_DynamicProp = (omniORB.tcInternal.tv_struct, DynamicProp, DynamicProp._NP_RepositoryId, 'DynamicProp', 'eval_if', omniORB.typeMapping['IDL:omg.org/CosTradingDynamic/DynamicPropEval:1.0'], 'returned_type', omniORB.tcInternal.tv_TypeCode, 'extra_info', omniORB.tcInternal.tv_any)
_0_CosTradingDynamic._tc_DynamicProp = omniORB.tcInternal.createTypeCode(_0_CosTradingDynamic._d_DynamicProp)
omniORB.registerType(DynamicProp._NP_RepositoryId, _0_CosTradingDynamic._d_DynamicProp, _0_CosTradingDynamic._tc_DynamicProp)
del DynamicProp
__name__ = 'CosTradingDynamic_idl'
_exported_modules = ('CosTradingDynamic', )