# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./CosTypedEventChannelAdmin_idl.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 19292 bytes
import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA
_omnipy.checkVersion(4, 2, __file__, 1)
try:
    property
except NameError:

    def property(*args):
        pass


import CosEventComm_idl
_0_CosEventComm = omniORB.openModule('CosEventComm')
_0_CosEventComm__POA = omniORB.openModule('CosEventComm__POA')
import CosEventChannelAdmin_idl
_0_CosEventChannelAdmin = omniORB.openModule('CosEventChannelAdmin')
_0_CosEventChannelAdmin__POA = omniORB.openModule('CosEventChannelAdmin__POA')
import CosTypedEventComm_idl
_0_CosTypedEventComm = omniORB.openModule('CosTypedEventComm')
_0_CosTypedEventComm__POA = omniORB.openModule('CosTypedEventComm__POA')
__name__ = 'CosTypedEventChannelAdmin'
_0_CosTypedEventChannelAdmin = omniORB.openModule('CosTypedEventChannelAdmin', '/tmp/corba/omni/share/idl/omniORB/COS/CosTypedEventChannelAdmin.idl')
_0_CosTypedEventChannelAdmin__POA = omniORB.openModule('CosTypedEventChannelAdmin__POA', '/tmp/corba/omni/share/idl/omniORB/COS/CosTypedEventChannelAdmin.idl')
_0_CosTypedEventChannelAdmin.InterfaceNotSupported = omniORB.newEmptyClass()

class InterfaceNotSupported(CORBA.UserException):
    _NP_RepositoryId = 'IDL:omg.org/CosTypedEventChannelAdmin/InterfaceNotSupported:1.0'

    def __init__(self):
        CORBA.UserException.__init__(self)


_0_CosTypedEventChannelAdmin.InterfaceNotSupported = InterfaceNotSupported
_0_CosTypedEventChannelAdmin._d_InterfaceNotSupported = (omniORB.tcInternal.tv_except, InterfaceNotSupported, InterfaceNotSupported._NP_RepositoryId, 'InterfaceNotSupported')
_0_CosTypedEventChannelAdmin._tc_InterfaceNotSupported = omniORB.tcInternal.createTypeCode(_0_CosTypedEventChannelAdmin._d_InterfaceNotSupported)
omniORB.registerType(InterfaceNotSupported._NP_RepositoryId, _0_CosTypedEventChannelAdmin._d_InterfaceNotSupported, _0_CosTypedEventChannelAdmin._tc_InterfaceNotSupported)
del InterfaceNotSupported
_0_CosTypedEventChannelAdmin.NoSuchImplementation = omniORB.newEmptyClass()

class NoSuchImplementation(CORBA.UserException):
    _NP_RepositoryId = 'IDL:omg.org/CosTypedEventChannelAdmin/NoSuchImplementation:1.0'

    def __init__(self):
        CORBA.UserException.__init__(self)


_0_CosTypedEventChannelAdmin.NoSuchImplementation = NoSuchImplementation
_0_CosTypedEventChannelAdmin._d_NoSuchImplementation = (omniORB.tcInternal.tv_except, NoSuchImplementation, NoSuchImplementation._NP_RepositoryId, 'NoSuchImplementation')
_0_CosTypedEventChannelAdmin._tc_NoSuchImplementation = omniORB.tcInternal.createTypeCode(_0_CosTypedEventChannelAdmin._d_NoSuchImplementation)
omniORB.registerType(NoSuchImplementation._NP_RepositoryId, _0_CosTypedEventChannelAdmin._d_NoSuchImplementation, _0_CosTypedEventChannelAdmin._tc_NoSuchImplementation)
del NoSuchImplementation

class Key:
    _NP_RepositoryId = 'IDL:omg.org/CosTypedEventChannelAdmin/Key:1.0'

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')


_0_CosTypedEventChannelAdmin.Key = Key
_0_CosTypedEventChannelAdmin._d_Key = (omniORB.tcInternal.tv_string, 0)
_0_CosTypedEventChannelAdmin._ad_Key = (omniORB.tcInternal.tv_alias, Key._NP_RepositoryId, 'Key', (omniORB.tcInternal.tv_string, 0))
_0_CosTypedEventChannelAdmin._tc_Key = omniORB.tcInternal.createTypeCode(_0_CosTypedEventChannelAdmin._ad_Key)
omniORB.registerType(Key._NP_RepositoryId, _0_CosTypedEventChannelAdmin._ad_Key, _0_CosTypedEventChannelAdmin._tc_Key)
del Key
_0_CosTypedEventChannelAdmin._d_TypedProxyPushConsumer = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosTypedEventChannelAdmin/TypedProxyPushConsumer:1.0', 'TypedProxyPushConsumer')
omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/TypedProxyPushConsumer:1.0'] = _0_CosTypedEventChannelAdmin._d_TypedProxyPushConsumer
_0_CosTypedEventChannelAdmin.TypedProxyPushConsumer = omniORB.newEmptyClass()

class TypedProxyPushConsumer(_0_CosEventChannelAdmin.ProxyPushConsumer, _0_CosTypedEventComm.TypedPushConsumer):
    _NP_RepositoryId = _0_CosTypedEventChannelAdmin._d_TypedProxyPushConsumer[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosTypedEventChannelAdmin.TypedProxyPushConsumer = TypedProxyPushConsumer
_0_CosTypedEventChannelAdmin._tc_TypedProxyPushConsumer = omniORB.tcInternal.createTypeCode(_0_CosTypedEventChannelAdmin._d_TypedProxyPushConsumer)
omniORB.registerType(TypedProxyPushConsumer._NP_RepositoryId, _0_CosTypedEventChannelAdmin._d_TypedProxyPushConsumer, _0_CosTypedEventChannelAdmin._tc_TypedProxyPushConsumer)

class _objref_TypedProxyPushConsumer(_0_CosEventChannelAdmin._objref_ProxyPushConsumer, _0_CosTypedEventComm._objref_TypedPushConsumer):
    _NP_RepositoryId = TypedProxyPushConsumer._NP_RepositoryId

    def __init__(self, obj):
        _0_CosEventChannelAdmin._objref_ProxyPushConsumer.__init__(self, obj)
        _0_CosTypedEventComm._objref_TypedPushConsumer.__init__(self, obj)


omniORB.registerObjref(TypedProxyPushConsumer._NP_RepositoryId, _objref_TypedProxyPushConsumer)
_0_CosTypedEventChannelAdmin._objref_TypedProxyPushConsumer = _objref_TypedProxyPushConsumer
del TypedProxyPushConsumer
del _objref_TypedProxyPushConsumer
__name__ = 'CosTypedEventChannelAdmin__POA'

class TypedProxyPushConsumer(_0_CosEventChannelAdmin__POA.ProxyPushConsumer, _0_CosTypedEventComm__POA.TypedPushConsumer):
    _NP_RepositoryId = _0_CosTypedEventChannelAdmin.TypedProxyPushConsumer._NP_RepositoryId
    _omni_op_d = {}
    _omni_op_d.update(_0_CosEventChannelAdmin__POA.ProxyPushConsumer._omni_op_d)
    _omni_op_d.update(_0_CosTypedEventComm__POA.TypedPushConsumer._omni_op_d)


TypedProxyPushConsumer._omni_skeleton = TypedProxyPushConsumer
_0_CosTypedEventChannelAdmin__POA.TypedProxyPushConsumer = TypedProxyPushConsumer
omniORB.registerSkeleton(TypedProxyPushConsumer._NP_RepositoryId, TypedProxyPushConsumer)
del TypedProxyPushConsumer
__name__ = 'CosTypedEventChannelAdmin'
_0_CosTypedEventChannelAdmin._d_TypedProxyPullSupplier = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosTypedEventChannelAdmin/TypedProxyPullSupplier:1.0', 'TypedProxyPullSupplier')
omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/TypedProxyPullSupplier:1.0'] = _0_CosTypedEventChannelAdmin._d_TypedProxyPullSupplier
_0_CosTypedEventChannelAdmin.TypedProxyPullSupplier = omniORB.newEmptyClass()

class TypedProxyPullSupplier(_0_CosEventChannelAdmin.ProxyPullSupplier, _0_CosTypedEventComm.TypedPullSupplier):
    _NP_RepositoryId = _0_CosTypedEventChannelAdmin._d_TypedProxyPullSupplier[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosTypedEventChannelAdmin.TypedProxyPullSupplier = TypedProxyPullSupplier
_0_CosTypedEventChannelAdmin._tc_TypedProxyPullSupplier = omniORB.tcInternal.createTypeCode(_0_CosTypedEventChannelAdmin._d_TypedProxyPullSupplier)
omniORB.registerType(TypedProxyPullSupplier._NP_RepositoryId, _0_CosTypedEventChannelAdmin._d_TypedProxyPullSupplier, _0_CosTypedEventChannelAdmin._tc_TypedProxyPullSupplier)

class _objref_TypedProxyPullSupplier(_0_CosEventChannelAdmin._objref_ProxyPullSupplier, _0_CosTypedEventComm._objref_TypedPullSupplier):
    _NP_RepositoryId = TypedProxyPullSupplier._NP_RepositoryId

    def __init__(self, obj):
        _0_CosEventChannelAdmin._objref_ProxyPullSupplier.__init__(self, obj)
        _0_CosTypedEventComm._objref_TypedPullSupplier.__init__(self, obj)


omniORB.registerObjref(TypedProxyPullSupplier._NP_RepositoryId, _objref_TypedProxyPullSupplier)
_0_CosTypedEventChannelAdmin._objref_TypedProxyPullSupplier = _objref_TypedProxyPullSupplier
del TypedProxyPullSupplier
del _objref_TypedProxyPullSupplier
__name__ = 'CosTypedEventChannelAdmin__POA'

class TypedProxyPullSupplier(_0_CosEventChannelAdmin__POA.ProxyPullSupplier, _0_CosTypedEventComm__POA.TypedPullSupplier):
    _NP_RepositoryId = _0_CosTypedEventChannelAdmin.TypedProxyPullSupplier._NP_RepositoryId
    _omni_op_d = {}
    _omni_op_d.update(_0_CosEventChannelAdmin__POA.ProxyPullSupplier._omni_op_d)
    _omni_op_d.update(_0_CosTypedEventComm__POA.TypedPullSupplier._omni_op_d)


TypedProxyPullSupplier._omni_skeleton = TypedProxyPullSupplier
_0_CosTypedEventChannelAdmin__POA.TypedProxyPullSupplier = TypedProxyPullSupplier
omniORB.registerSkeleton(TypedProxyPullSupplier._NP_RepositoryId, TypedProxyPullSupplier)
del TypedProxyPullSupplier
__name__ = 'CosTypedEventChannelAdmin'
_0_CosTypedEventChannelAdmin._d_TypedSupplierAdmin = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosTypedEventChannelAdmin/TypedSupplierAdmin:1.0', 'TypedSupplierAdmin')
omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/TypedSupplierAdmin:1.0'] = _0_CosTypedEventChannelAdmin._d_TypedSupplierAdmin
_0_CosTypedEventChannelAdmin.TypedSupplierAdmin = omniORB.newEmptyClass()

class TypedSupplierAdmin(_0_CosEventChannelAdmin.SupplierAdmin):
    _NP_RepositoryId = _0_CosTypedEventChannelAdmin._d_TypedSupplierAdmin[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosTypedEventChannelAdmin.TypedSupplierAdmin = TypedSupplierAdmin
_0_CosTypedEventChannelAdmin._tc_TypedSupplierAdmin = omniORB.tcInternal.createTypeCode(_0_CosTypedEventChannelAdmin._d_TypedSupplierAdmin)
omniORB.registerType(TypedSupplierAdmin._NP_RepositoryId, _0_CosTypedEventChannelAdmin._d_TypedSupplierAdmin, _0_CosTypedEventChannelAdmin._tc_TypedSupplierAdmin)
TypedSupplierAdmin._d_obtain_typed_push_consumer = (
 (
  omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/Key:1.0'],), (omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/TypedProxyPushConsumer:1.0'],), {_0_CosTypedEventChannelAdmin.InterfaceNotSupported._NP_RepositoryId: _0_CosTypedEventChannelAdmin._d_InterfaceNotSupported})
TypedSupplierAdmin._d_obtain_typed_pull_consumer = ((omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/Key:1.0'],), (omniORB.typeMapping['IDL:omg.org/CosEventChannelAdmin/ProxyPullConsumer:1.0'],), {_0_CosTypedEventChannelAdmin.NoSuchImplementation._NP_RepositoryId: _0_CosTypedEventChannelAdmin._d_NoSuchImplementation})

class _objref_TypedSupplierAdmin(_0_CosEventChannelAdmin._objref_SupplierAdmin):
    _NP_RepositoryId = TypedSupplierAdmin._NP_RepositoryId

    def __init__(self, obj):
        _0_CosEventChannelAdmin._objref_SupplierAdmin.__init__(self, obj)

    def obtain_typed_push_consumer(self, *args):
        return self._obj.invoke('obtain_typed_push_consumer', _0_CosTypedEventChannelAdmin.TypedSupplierAdmin._d_obtain_typed_push_consumer, args)

    def obtain_typed_pull_consumer(self, *args):
        return self._obj.invoke('obtain_typed_pull_consumer', _0_CosTypedEventChannelAdmin.TypedSupplierAdmin._d_obtain_typed_pull_consumer, args)


omniORB.registerObjref(TypedSupplierAdmin._NP_RepositoryId, _objref_TypedSupplierAdmin)
_0_CosTypedEventChannelAdmin._objref_TypedSupplierAdmin = _objref_TypedSupplierAdmin
del TypedSupplierAdmin
del _objref_TypedSupplierAdmin
__name__ = 'CosTypedEventChannelAdmin__POA'

class TypedSupplierAdmin(_0_CosEventChannelAdmin__POA.SupplierAdmin):
    _NP_RepositoryId = _0_CosTypedEventChannelAdmin.TypedSupplierAdmin._NP_RepositoryId
    _omni_op_d = {'obtain_typed_push_consumer':_0_CosTypedEventChannelAdmin.TypedSupplierAdmin._d_obtain_typed_push_consumer, 
     'obtain_typed_pull_consumer':_0_CosTypedEventChannelAdmin.TypedSupplierAdmin._d_obtain_typed_pull_consumer}
    _omni_op_d.update(_0_CosEventChannelAdmin__POA.SupplierAdmin._omni_op_d)


TypedSupplierAdmin._omni_skeleton = TypedSupplierAdmin
_0_CosTypedEventChannelAdmin__POA.TypedSupplierAdmin = TypedSupplierAdmin
omniORB.registerSkeleton(TypedSupplierAdmin._NP_RepositoryId, TypedSupplierAdmin)
del TypedSupplierAdmin
__name__ = 'CosTypedEventChannelAdmin'
_0_CosTypedEventChannelAdmin._d_TypedConsumerAdmin = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosTypedEventChannelAdmin/TypedConsumerAdmin:1.0', 'TypedConsumerAdmin')
omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/TypedConsumerAdmin:1.0'] = _0_CosTypedEventChannelAdmin._d_TypedConsumerAdmin
_0_CosTypedEventChannelAdmin.TypedConsumerAdmin = omniORB.newEmptyClass()

class TypedConsumerAdmin(_0_CosEventChannelAdmin.ConsumerAdmin):
    _NP_RepositoryId = _0_CosTypedEventChannelAdmin._d_TypedConsumerAdmin[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosTypedEventChannelAdmin.TypedConsumerAdmin = TypedConsumerAdmin
_0_CosTypedEventChannelAdmin._tc_TypedConsumerAdmin = omniORB.tcInternal.createTypeCode(_0_CosTypedEventChannelAdmin._d_TypedConsumerAdmin)
omniORB.registerType(TypedConsumerAdmin._NP_RepositoryId, _0_CosTypedEventChannelAdmin._d_TypedConsumerAdmin, _0_CosTypedEventChannelAdmin._tc_TypedConsumerAdmin)
TypedConsumerAdmin._d_obtain_typed_pull_supplier = (
 (
  omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/Key:1.0'],), (omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/TypedProxyPullSupplier:1.0'],), {_0_CosTypedEventChannelAdmin.InterfaceNotSupported._NP_RepositoryId: _0_CosTypedEventChannelAdmin._d_InterfaceNotSupported})
TypedConsumerAdmin._d_obtain_typed_push_supplier = ((omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/Key:1.0'],), (omniORB.typeMapping['IDL:omg.org/CosEventChannelAdmin/ProxyPushSupplier:1.0'],), {_0_CosTypedEventChannelAdmin.NoSuchImplementation._NP_RepositoryId: _0_CosTypedEventChannelAdmin._d_NoSuchImplementation})

class _objref_TypedConsumerAdmin(_0_CosEventChannelAdmin._objref_ConsumerAdmin):
    _NP_RepositoryId = TypedConsumerAdmin._NP_RepositoryId

    def __init__(self, obj):
        _0_CosEventChannelAdmin._objref_ConsumerAdmin.__init__(self, obj)

    def obtain_typed_pull_supplier(self, *args):
        return self._obj.invoke('obtain_typed_pull_supplier', _0_CosTypedEventChannelAdmin.TypedConsumerAdmin._d_obtain_typed_pull_supplier, args)

    def obtain_typed_push_supplier(self, *args):
        return self._obj.invoke('obtain_typed_push_supplier', _0_CosTypedEventChannelAdmin.TypedConsumerAdmin._d_obtain_typed_push_supplier, args)


omniORB.registerObjref(TypedConsumerAdmin._NP_RepositoryId, _objref_TypedConsumerAdmin)
_0_CosTypedEventChannelAdmin._objref_TypedConsumerAdmin = _objref_TypedConsumerAdmin
del TypedConsumerAdmin
del _objref_TypedConsumerAdmin
__name__ = 'CosTypedEventChannelAdmin__POA'

class TypedConsumerAdmin(_0_CosEventChannelAdmin__POA.ConsumerAdmin):
    _NP_RepositoryId = _0_CosTypedEventChannelAdmin.TypedConsumerAdmin._NP_RepositoryId
    _omni_op_d = {'obtain_typed_pull_supplier':_0_CosTypedEventChannelAdmin.TypedConsumerAdmin._d_obtain_typed_pull_supplier, 
     'obtain_typed_push_supplier':_0_CosTypedEventChannelAdmin.TypedConsumerAdmin._d_obtain_typed_push_supplier}
    _omni_op_d.update(_0_CosEventChannelAdmin__POA.ConsumerAdmin._omni_op_d)


TypedConsumerAdmin._omni_skeleton = TypedConsumerAdmin
_0_CosTypedEventChannelAdmin__POA.TypedConsumerAdmin = TypedConsumerAdmin
omniORB.registerSkeleton(TypedConsumerAdmin._NP_RepositoryId, TypedConsumerAdmin)
del TypedConsumerAdmin
__name__ = 'CosTypedEventChannelAdmin'
_0_CosTypedEventChannelAdmin._d_TypedEventChannel = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosTypedEventChannelAdmin/TypedEventChannel:1.0', 'TypedEventChannel')
omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/TypedEventChannel:1.0'] = _0_CosTypedEventChannelAdmin._d_TypedEventChannel
_0_CosTypedEventChannelAdmin.TypedEventChannel = omniORB.newEmptyClass()

class TypedEventChannel:
    _NP_RepositoryId = _0_CosTypedEventChannelAdmin._d_TypedEventChannel[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosTypedEventChannelAdmin.TypedEventChannel = TypedEventChannel
_0_CosTypedEventChannelAdmin._tc_TypedEventChannel = omniORB.tcInternal.createTypeCode(_0_CosTypedEventChannelAdmin._d_TypedEventChannel)
omniORB.registerType(TypedEventChannel._NP_RepositoryId, _0_CosTypedEventChannelAdmin._d_TypedEventChannel, _0_CosTypedEventChannelAdmin._tc_TypedEventChannel)
TypedEventChannel._d_for_consumers = ((), (omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/TypedConsumerAdmin:1.0'],), None)
TypedEventChannel._d_for_suppliers = ((), (omniORB.typeMapping['IDL:omg.org/CosTypedEventChannelAdmin/TypedSupplierAdmin:1.0'],), None)
TypedEventChannel._d_destroy = ((), (), None)

class _objref_TypedEventChannel(CORBA.Object):
    _NP_RepositoryId = TypedEventChannel._NP_RepositoryId

    def __init__(self, obj):
        CORBA.Object.__init__(self, obj)

    def for_consumers(self, *args):
        return self._obj.invoke('for_consumers', _0_CosTypedEventChannelAdmin.TypedEventChannel._d_for_consumers, args)

    def for_suppliers(self, *args):
        return self._obj.invoke('for_suppliers', _0_CosTypedEventChannelAdmin.TypedEventChannel._d_for_suppliers, args)

    def destroy(self, *args):
        return self._obj.invoke('destroy', _0_CosTypedEventChannelAdmin.TypedEventChannel._d_destroy, args)


omniORB.registerObjref(TypedEventChannel._NP_RepositoryId, _objref_TypedEventChannel)
_0_CosTypedEventChannelAdmin._objref_TypedEventChannel = _objref_TypedEventChannel
del TypedEventChannel
del _objref_TypedEventChannel
__name__ = 'CosTypedEventChannelAdmin__POA'

class TypedEventChannel(PortableServer.Servant):
    _NP_RepositoryId = _0_CosTypedEventChannelAdmin.TypedEventChannel._NP_RepositoryId
    _omni_op_d = {'for_consumers':_0_CosTypedEventChannelAdmin.TypedEventChannel._d_for_consumers, 
     'for_suppliers':_0_CosTypedEventChannelAdmin.TypedEventChannel._d_for_suppliers,  'destroy':_0_CosTypedEventChannelAdmin.TypedEventChannel._d_destroy}


TypedEventChannel._omni_skeleton = TypedEventChannel
_0_CosTypedEventChannelAdmin__POA.TypedEventChannel = TypedEventChannel
omniORB.registerSkeleton(TypedEventChannel._NP_RepositoryId, TypedEventChannel)
del TypedEventChannel
__name__ = 'CosTypedEventChannelAdmin'
__name__ = 'CosTypedEventChannelAdmin_idl'
_exported_modules = ('CosTypedEventChannelAdmin', )