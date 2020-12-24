# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./CosNotifyComm_idl.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 37465 bytes
import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA
_omnipy.checkVersion(4, 2, __file__, 1)
try:
    property
except NameError:

    def property(*args):
        pass


import CosNotification_idl
_0_CosNotification = omniORB.openModule('CosNotification')
_0_CosNotification__POA = omniORB.openModule('CosNotification__POA')
import CosEventComm_idl
_0_CosEventComm = omniORB.openModule('CosEventComm')
_0_CosEventComm__POA = omniORB.openModule('CosEventComm__POA')
__name__ = 'CosNotifyComm'
_0_CosNotifyComm = omniORB.openModule('CosNotifyComm', '/tmp/corba/omni/share/idl/omniORB/COS/CosNotifyComm.idl')
_0_CosNotifyComm__POA = omniORB.openModule('CosNotifyComm__POA', '/tmp/corba/omni/share/idl/omniORB/COS/CosNotifyComm.idl')
_0_CosNotifyComm.InvalidEventType = omniORB.newEmptyClass()

class InvalidEventType(CORBA.UserException):
    _NP_RepositoryId = 'IDL:omg.org/CosNotifyComm/InvalidEventType:1.0'

    def __init__(self, type):
        CORBA.UserException.__init__(self, type)
        self.type = type


_0_CosNotifyComm.InvalidEventType = InvalidEventType
_0_CosNotifyComm._d_InvalidEventType = (omniORB.tcInternal.tv_except, InvalidEventType, InvalidEventType._NP_RepositoryId, 'InvalidEventType', 'type', omniORB.typeMapping['IDL:omg.org/CosNotification/EventType:1.0'])
_0_CosNotifyComm._tc_InvalidEventType = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_InvalidEventType)
omniORB.registerType(InvalidEventType._NP_RepositoryId, _0_CosNotifyComm._d_InvalidEventType, _0_CosNotifyComm._tc_InvalidEventType)
del InvalidEventType
_0_CosNotifyComm._d_NotifyPublish = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/NotifyPublish:1.0', 'NotifyPublish')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/NotifyPublish:1.0'] = _0_CosNotifyComm._d_NotifyPublish
_0_CosNotifyComm.NotifyPublish = omniORB.newEmptyClass()

class NotifyPublish:
    _NP_RepositoryId = _0_CosNotifyComm._d_NotifyPublish[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.NotifyPublish = NotifyPublish
_0_CosNotifyComm._tc_NotifyPublish = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_NotifyPublish)
omniORB.registerType(NotifyPublish._NP_RepositoryId, _0_CosNotifyComm._d_NotifyPublish, _0_CosNotifyComm._tc_NotifyPublish)
NotifyPublish._d_offer_change = (
 (
  omniORB.typeMapping['IDL:omg.org/CosNotification/EventTypeSeq:1.0'], omniORB.typeMapping['IDL:omg.org/CosNotification/EventTypeSeq:1.0']), (), {_0_CosNotifyComm.InvalidEventType._NP_RepositoryId: _0_CosNotifyComm._d_InvalidEventType})

class _objref_NotifyPublish(CORBA.Object):
    _NP_RepositoryId = NotifyPublish._NP_RepositoryId

    def __init__(self, obj):
        CORBA.Object.__init__(self, obj)

    def offer_change(self, *args):
        return self._obj.invoke('offer_change', _0_CosNotifyComm.NotifyPublish._d_offer_change, args)


omniORB.registerObjref(NotifyPublish._NP_RepositoryId, _objref_NotifyPublish)
_0_CosNotifyComm._objref_NotifyPublish = _objref_NotifyPublish
del NotifyPublish
del _objref_NotifyPublish
__name__ = 'CosNotifyComm__POA'

class NotifyPublish(PortableServer.Servant):
    _NP_RepositoryId = _0_CosNotifyComm.NotifyPublish._NP_RepositoryId
    _omni_op_d = {'offer_change': _0_CosNotifyComm.NotifyPublish._d_offer_change}


NotifyPublish._omni_skeleton = NotifyPublish
_0_CosNotifyComm__POA.NotifyPublish = NotifyPublish
omniORB.registerSkeleton(NotifyPublish._NP_RepositoryId, NotifyPublish)
del NotifyPublish
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_NotifySubscribe = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/NotifySubscribe:1.0', 'NotifySubscribe')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/NotifySubscribe:1.0'] = _0_CosNotifyComm._d_NotifySubscribe
_0_CosNotifyComm.NotifySubscribe = omniORB.newEmptyClass()

class NotifySubscribe:
    _NP_RepositoryId = _0_CosNotifyComm._d_NotifySubscribe[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.NotifySubscribe = NotifySubscribe
_0_CosNotifyComm._tc_NotifySubscribe = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_NotifySubscribe)
omniORB.registerType(NotifySubscribe._NP_RepositoryId, _0_CosNotifyComm._d_NotifySubscribe, _0_CosNotifyComm._tc_NotifySubscribe)
NotifySubscribe._d_subscription_change = (
 (
  omniORB.typeMapping['IDL:omg.org/CosNotification/EventTypeSeq:1.0'], omniORB.typeMapping['IDL:omg.org/CosNotification/EventTypeSeq:1.0']), (), {_0_CosNotifyComm.InvalidEventType._NP_RepositoryId: _0_CosNotifyComm._d_InvalidEventType})

class _objref_NotifySubscribe(CORBA.Object):
    _NP_RepositoryId = NotifySubscribe._NP_RepositoryId

    def __init__(self, obj):
        CORBA.Object.__init__(self, obj)

    def subscription_change(self, *args):
        return self._obj.invoke('subscription_change', _0_CosNotifyComm.NotifySubscribe._d_subscription_change, args)


omniORB.registerObjref(NotifySubscribe._NP_RepositoryId, _objref_NotifySubscribe)
_0_CosNotifyComm._objref_NotifySubscribe = _objref_NotifySubscribe
del NotifySubscribe
del _objref_NotifySubscribe
__name__ = 'CosNotifyComm__POA'

class NotifySubscribe(PortableServer.Servant):
    _NP_RepositoryId = _0_CosNotifyComm.NotifySubscribe._NP_RepositoryId
    _omni_op_d = {'subscription_change': _0_CosNotifyComm.NotifySubscribe._d_subscription_change}


NotifySubscribe._omni_skeleton = NotifySubscribe
_0_CosNotifyComm__POA.NotifySubscribe = NotifySubscribe
omniORB.registerSkeleton(NotifySubscribe._NP_RepositoryId, NotifySubscribe)
del NotifySubscribe
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_PushConsumer = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/PushConsumer:1.0', 'PushConsumer')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/PushConsumer:1.0'] = _0_CosNotifyComm._d_PushConsumer
_0_CosNotifyComm.PushConsumer = omniORB.newEmptyClass()

class PushConsumer(_0_CosNotifyComm.NotifyPublish, _0_CosEventComm.PushConsumer):
    _NP_RepositoryId = _0_CosNotifyComm._d_PushConsumer[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.PushConsumer = PushConsumer
_0_CosNotifyComm._tc_PushConsumer = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_PushConsumer)
omniORB.registerType(PushConsumer._NP_RepositoryId, _0_CosNotifyComm._d_PushConsumer, _0_CosNotifyComm._tc_PushConsumer)

class _objref_PushConsumer(_0_CosNotifyComm._objref_NotifyPublish, _0_CosEventComm._objref_PushConsumer):
    _NP_RepositoryId = PushConsumer._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifyPublish.__init__(self, obj)
        _0_CosEventComm._objref_PushConsumer.__init__(self, obj)


omniORB.registerObjref(PushConsumer._NP_RepositoryId, _objref_PushConsumer)
_0_CosNotifyComm._objref_PushConsumer = _objref_PushConsumer
del PushConsumer
del _objref_PushConsumer
__name__ = 'CosNotifyComm__POA'

class PushConsumer(_0_CosNotifyComm__POA.NotifyPublish, _0_CosEventComm__POA.PushConsumer):
    _NP_RepositoryId = _0_CosNotifyComm.PushConsumer._NP_RepositoryId
    _omni_op_d = {}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifyPublish._omni_op_d)
    _omni_op_d.update(_0_CosEventComm__POA.PushConsumer._omni_op_d)


PushConsumer._omni_skeleton = PushConsumer
_0_CosNotifyComm__POA.PushConsumer = PushConsumer
omniORB.registerSkeleton(PushConsumer._NP_RepositoryId, PushConsumer)
del PushConsumer
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_PullConsumer = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/PullConsumer:1.0', 'PullConsumer')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/PullConsumer:1.0'] = _0_CosNotifyComm._d_PullConsumer
_0_CosNotifyComm.PullConsumer = omniORB.newEmptyClass()

class PullConsumer(_0_CosNotifyComm.NotifyPublish, _0_CosEventComm.PullConsumer):
    _NP_RepositoryId = _0_CosNotifyComm._d_PullConsumer[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.PullConsumer = PullConsumer
_0_CosNotifyComm._tc_PullConsumer = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_PullConsumer)
omniORB.registerType(PullConsumer._NP_RepositoryId, _0_CosNotifyComm._d_PullConsumer, _0_CosNotifyComm._tc_PullConsumer)

class _objref_PullConsumer(_0_CosNotifyComm._objref_NotifyPublish, _0_CosEventComm._objref_PullConsumer):
    _NP_RepositoryId = PullConsumer._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifyPublish.__init__(self, obj)
        _0_CosEventComm._objref_PullConsumer.__init__(self, obj)


omniORB.registerObjref(PullConsumer._NP_RepositoryId, _objref_PullConsumer)
_0_CosNotifyComm._objref_PullConsumer = _objref_PullConsumer
del PullConsumer
del _objref_PullConsumer
__name__ = 'CosNotifyComm__POA'

class PullConsumer(_0_CosNotifyComm__POA.NotifyPublish, _0_CosEventComm__POA.PullConsumer):
    _NP_RepositoryId = _0_CosNotifyComm.PullConsumer._NP_RepositoryId
    _omni_op_d = {}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifyPublish._omni_op_d)
    _omni_op_d.update(_0_CosEventComm__POA.PullConsumer._omni_op_d)


PullConsumer._omni_skeleton = PullConsumer
_0_CosNotifyComm__POA.PullConsumer = PullConsumer
omniORB.registerSkeleton(PullConsumer._NP_RepositoryId, PullConsumer)
del PullConsumer
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_PullSupplier = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/PullSupplier:1.0', 'PullSupplier')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/PullSupplier:1.0'] = _0_CosNotifyComm._d_PullSupplier
_0_CosNotifyComm.PullSupplier = omniORB.newEmptyClass()

class PullSupplier(_0_CosNotifyComm.NotifySubscribe, _0_CosEventComm.PullSupplier):
    _NP_RepositoryId = _0_CosNotifyComm._d_PullSupplier[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.PullSupplier = PullSupplier
_0_CosNotifyComm._tc_PullSupplier = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_PullSupplier)
omniORB.registerType(PullSupplier._NP_RepositoryId, _0_CosNotifyComm._d_PullSupplier, _0_CosNotifyComm._tc_PullSupplier)

class _objref_PullSupplier(_0_CosNotifyComm._objref_NotifySubscribe, _0_CosEventComm._objref_PullSupplier):
    _NP_RepositoryId = PullSupplier._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifySubscribe.__init__(self, obj)
        _0_CosEventComm._objref_PullSupplier.__init__(self, obj)


omniORB.registerObjref(PullSupplier._NP_RepositoryId, _objref_PullSupplier)
_0_CosNotifyComm._objref_PullSupplier = _objref_PullSupplier
del PullSupplier
del _objref_PullSupplier
__name__ = 'CosNotifyComm__POA'

class PullSupplier(_0_CosNotifyComm__POA.NotifySubscribe, _0_CosEventComm__POA.PullSupplier):
    _NP_RepositoryId = _0_CosNotifyComm.PullSupplier._NP_RepositoryId
    _omni_op_d = {}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifySubscribe._omni_op_d)
    _omni_op_d.update(_0_CosEventComm__POA.PullSupplier._omni_op_d)


PullSupplier._omni_skeleton = PullSupplier
_0_CosNotifyComm__POA.PullSupplier = PullSupplier
omniORB.registerSkeleton(PullSupplier._NP_RepositoryId, PullSupplier)
del PullSupplier
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_PushSupplier = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/PushSupplier:1.0', 'PushSupplier')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/PushSupplier:1.0'] = _0_CosNotifyComm._d_PushSupplier
_0_CosNotifyComm.PushSupplier = omniORB.newEmptyClass()

class PushSupplier(_0_CosNotifyComm.NotifySubscribe, _0_CosEventComm.PushSupplier):
    _NP_RepositoryId = _0_CosNotifyComm._d_PushSupplier[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.PushSupplier = PushSupplier
_0_CosNotifyComm._tc_PushSupplier = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_PushSupplier)
omniORB.registerType(PushSupplier._NP_RepositoryId, _0_CosNotifyComm._d_PushSupplier, _0_CosNotifyComm._tc_PushSupplier)

class _objref_PushSupplier(_0_CosNotifyComm._objref_NotifySubscribe, _0_CosEventComm._objref_PushSupplier):
    _NP_RepositoryId = PushSupplier._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifySubscribe.__init__(self, obj)
        _0_CosEventComm._objref_PushSupplier.__init__(self, obj)


omniORB.registerObjref(PushSupplier._NP_RepositoryId, _objref_PushSupplier)
_0_CosNotifyComm._objref_PushSupplier = _objref_PushSupplier
del PushSupplier
del _objref_PushSupplier
__name__ = 'CosNotifyComm__POA'

class PushSupplier(_0_CosNotifyComm__POA.NotifySubscribe, _0_CosEventComm__POA.PushSupplier):
    _NP_RepositoryId = _0_CosNotifyComm.PushSupplier._NP_RepositoryId
    _omni_op_d = {}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifySubscribe._omni_op_d)
    _omni_op_d.update(_0_CosEventComm__POA.PushSupplier._omni_op_d)


PushSupplier._omni_skeleton = PushSupplier
_0_CosNotifyComm__POA.PushSupplier = PushSupplier
omniORB.registerSkeleton(PushSupplier._NP_RepositoryId, PushSupplier)
del PushSupplier
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_StructuredPushConsumer = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/StructuredPushConsumer:1.0', 'StructuredPushConsumer')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/StructuredPushConsumer:1.0'] = _0_CosNotifyComm._d_StructuredPushConsumer
_0_CosNotifyComm.StructuredPushConsumer = omniORB.newEmptyClass()

class StructuredPushConsumer(_0_CosNotifyComm.NotifyPublish):
    _NP_RepositoryId = _0_CosNotifyComm._d_StructuredPushConsumer[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.StructuredPushConsumer = StructuredPushConsumer
_0_CosNotifyComm._tc_StructuredPushConsumer = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_StructuredPushConsumer)
omniORB.registerType(StructuredPushConsumer._NP_RepositoryId, _0_CosNotifyComm._d_StructuredPushConsumer, _0_CosNotifyComm._tc_StructuredPushConsumer)
StructuredPushConsumer._d_push_structured_event = (
 (
  omniORB.typeMapping['IDL:omg.org/CosNotification/StructuredEvent:1.0'],), (), {_0_CosEventComm.Disconnected._NP_RepositoryId: _0_CosEventComm._d_Disconnected})
StructuredPushConsumer._d_disconnect_structured_push_consumer = ((), (), None)

class _objref_StructuredPushConsumer(_0_CosNotifyComm._objref_NotifyPublish):
    _NP_RepositoryId = StructuredPushConsumer._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifyPublish.__init__(self, obj)

    def push_structured_event(self, *args):
        return self._obj.invoke('push_structured_event', _0_CosNotifyComm.StructuredPushConsumer._d_push_structured_event, args)

    def disconnect_structured_push_consumer(self, *args):
        return self._obj.invoke('disconnect_structured_push_consumer', _0_CosNotifyComm.StructuredPushConsumer._d_disconnect_structured_push_consumer, args)


omniORB.registerObjref(StructuredPushConsumer._NP_RepositoryId, _objref_StructuredPushConsumer)
_0_CosNotifyComm._objref_StructuredPushConsumer = _objref_StructuredPushConsumer
del StructuredPushConsumer
del _objref_StructuredPushConsumer
__name__ = 'CosNotifyComm__POA'

class StructuredPushConsumer(_0_CosNotifyComm__POA.NotifyPublish):
    _NP_RepositoryId = _0_CosNotifyComm.StructuredPushConsumer._NP_RepositoryId
    _omni_op_d = {'push_structured_event':_0_CosNotifyComm.StructuredPushConsumer._d_push_structured_event, 
     'disconnect_structured_push_consumer':_0_CosNotifyComm.StructuredPushConsumer._d_disconnect_structured_push_consumer}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifyPublish._omni_op_d)


StructuredPushConsumer._omni_skeleton = StructuredPushConsumer
_0_CosNotifyComm__POA.StructuredPushConsumer = StructuredPushConsumer
omniORB.registerSkeleton(StructuredPushConsumer._NP_RepositoryId, StructuredPushConsumer)
del StructuredPushConsumer
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_StructuredPullConsumer = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/StructuredPullConsumer:1.0', 'StructuredPullConsumer')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/StructuredPullConsumer:1.0'] = _0_CosNotifyComm._d_StructuredPullConsumer
_0_CosNotifyComm.StructuredPullConsumer = omniORB.newEmptyClass()

class StructuredPullConsumer(_0_CosNotifyComm.NotifyPublish):
    _NP_RepositoryId = _0_CosNotifyComm._d_StructuredPullConsumer[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.StructuredPullConsumer = StructuredPullConsumer
_0_CosNotifyComm._tc_StructuredPullConsumer = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_StructuredPullConsumer)
omniORB.registerType(StructuredPullConsumer._NP_RepositoryId, _0_CosNotifyComm._d_StructuredPullConsumer, _0_CosNotifyComm._tc_StructuredPullConsumer)
StructuredPullConsumer._d_disconnect_structured_pull_consumer = ((), (), None)

class _objref_StructuredPullConsumer(_0_CosNotifyComm._objref_NotifyPublish):
    _NP_RepositoryId = StructuredPullConsumer._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifyPublish.__init__(self, obj)

    def disconnect_structured_pull_consumer(self, *args):
        return self._obj.invoke('disconnect_structured_pull_consumer', _0_CosNotifyComm.StructuredPullConsumer._d_disconnect_structured_pull_consumer, args)


omniORB.registerObjref(StructuredPullConsumer._NP_RepositoryId, _objref_StructuredPullConsumer)
_0_CosNotifyComm._objref_StructuredPullConsumer = _objref_StructuredPullConsumer
del StructuredPullConsumer
del _objref_StructuredPullConsumer
__name__ = 'CosNotifyComm__POA'

class StructuredPullConsumer(_0_CosNotifyComm__POA.NotifyPublish):
    _NP_RepositoryId = _0_CosNotifyComm.StructuredPullConsumer._NP_RepositoryId
    _omni_op_d = {'disconnect_structured_pull_consumer': _0_CosNotifyComm.StructuredPullConsumer._d_disconnect_structured_pull_consumer}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifyPublish._omni_op_d)


StructuredPullConsumer._omni_skeleton = StructuredPullConsumer
_0_CosNotifyComm__POA.StructuredPullConsumer = StructuredPullConsumer
omniORB.registerSkeleton(StructuredPullConsumer._NP_RepositoryId, StructuredPullConsumer)
del StructuredPullConsumer
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_StructuredPullSupplier = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/StructuredPullSupplier:1.0', 'StructuredPullSupplier')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/StructuredPullSupplier:1.0'] = _0_CosNotifyComm._d_StructuredPullSupplier
_0_CosNotifyComm.StructuredPullSupplier = omniORB.newEmptyClass()

class StructuredPullSupplier(_0_CosNotifyComm.NotifySubscribe):
    _NP_RepositoryId = _0_CosNotifyComm._d_StructuredPullSupplier[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.StructuredPullSupplier = StructuredPullSupplier
_0_CosNotifyComm._tc_StructuredPullSupplier = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_StructuredPullSupplier)
omniORB.registerType(StructuredPullSupplier._NP_RepositoryId, _0_CosNotifyComm._d_StructuredPullSupplier, _0_CosNotifyComm._tc_StructuredPullSupplier)
StructuredPullSupplier._d_pull_structured_event = ((), (omniORB.typeMapping['IDL:omg.org/CosNotification/StructuredEvent:1.0'],), {_0_CosEventComm.Disconnected._NP_RepositoryId: _0_CosEventComm._d_Disconnected})
StructuredPullSupplier._d_try_pull_structured_event = ((), (omniORB.typeMapping['IDL:omg.org/CosNotification/StructuredEvent:1.0'], omniORB.tcInternal.tv_boolean), {_0_CosEventComm.Disconnected._NP_RepositoryId: _0_CosEventComm._d_Disconnected})
StructuredPullSupplier._d_disconnect_structured_pull_supplier = ((), (), None)

class _objref_StructuredPullSupplier(_0_CosNotifyComm._objref_NotifySubscribe):
    _NP_RepositoryId = StructuredPullSupplier._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifySubscribe.__init__(self, obj)

    def pull_structured_event(self, *args):
        return self._obj.invoke('pull_structured_event', _0_CosNotifyComm.StructuredPullSupplier._d_pull_structured_event, args)

    def try_pull_structured_event(self, *args):
        return self._obj.invoke('try_pull_structured_event', _0_CosNotifyComm.StructuredPullSupplier._d_try_pull_structured_event, args)

    def disconnect_structured_pull_supplier(self, *args):
        return self._obj.invoke('disconnect_structured_pull_supplier', _0_CosNotifyComm.StructuredPullSupplier._d_disconnect_structured_pull_supplier, args)


omniORB.registerObjref(StructuredPullSupplier._NP_RepositoryId, _objref_StructuredPullSupplier)
_0_CosNotifyComm._objref_StructuredPullSupplier = _objref_StructuredPullSupplier
del StructuredPullSupplier
del _objref_StructuredPullSupplier
__name__ = 'CosNotifyComm__POA'

class StructuredPullSupplier(_0_CosNotifyComm__POA.NotifySubscribe):
    _NP_RepositoryId = _0_CosNotifyComm.StructuredPullSupplier._NP_RepositoryId
    _omni_op_d = {'pull_structured_event':_0_CosNotifyComm.StructuredPullSupplier._d_pull_structured_event, 
     'try_pull_structured_event':_0_CosNotifyComm.StructuredPullSupplier._d_try_pull_structured_event,  'disconnect_structured_pull_supplier':_0_CosNotifyComm.StructuredPullSupplier._d_disconnect_structured_pull_supplier}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifySubscribe._omni_op_d)


StructuredPullSupplier._omni_skeleton = StructuredPullSupplier
_0_CosNotifyComm__POA.StructuredPullSupplier = StructuredPullSupplier
omniORB.registerSkeleton(StructuredPullSupplier._NP_RepositoryId, StructuredPullSupplier)
del StructuredPullSupplier
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_StructuredPushSupplier = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/StructuredPushSupplier:1.0', 'StructuredPushSupplier')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/StructuredPushSupplier:1.0'] = _0_CosNotifyComm._d_StructuredPushSupplier
_0_CosNotifyComm.StructuredPushSupplier = omniORB.newEmptyClass()

class StructuredPushSupplier(_0_CosNotifyComm.NotifySubscribe):
    _NP_RepositoryId = _0_CosNotifyComm._d_StructuredPushSupplier[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.StructuredPushSupplier = StructuredPushSupplier
_0_CosNotifyComm._tc_StructuredPushSupplier = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_StructuredPushSupplier)
omniORB.registerType(StructuredPushSupplier._NP_RepositoryId, _0_CosNotifyComm._d_StructuredPushSupplier, _0_CosNotifyComm._tc_StructuredPushSupplier)
StructuredPushSupplier._d_disconnect_structured_push_supplier = ((), (), None)

class _objref_StructuredPushSupplier(_0_CosNotifyComm._objref_NotifySubscribe):
    _NP_RepositoryId = StructuredPushSupplier._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifySubscribe.__init__(self, obj)

    def disconnect_structured_push_supplier(self, *args):
        return self._obj.invoke('disconnect_structured_push_supplier', _0_CosNotifyComm.StructuredPushSupplier._d_disconnect_structured_push_supplier, args)


omniORB.registerObjref(StructuredPushSupplier._NP_RepositoryId, _objref_StructuredPushSupplier)
_0_CosNotifyComm._objref_StructuredPushSupplier = _objref_StructuredPushSupplier
del StructuredPushSupplier
del _objref_StructuredPushSupplier
__name__ = 'CosNotifyComm__POA'

class StructuredPushSupplier(_0_CosNotifyComm__POA.NotifySubscribe):
    _NP_RepositoryId = _0_CosNotifyComm.StructuredPushSupplier._NP_RepositoryId
    _omni_op_d = {'disconnect_structured_push_supplier': _0_CosNotifyComm.StructuredPushSupplier._d_disconnect_structured_push_supplier}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifySubscribe._omni_op_d)


StructuredPushSupplier._omni_skeleton = StructuredPushSupplier
_0_CosNotifyComm__POA.StructuredPushSupplier = StructuredPushSupplier
omniORB.registerSkeleton(StructuredPushSupplier._NP_RepositoryId, StructuredPushSupplier)
del StructuredPushSupplier
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_SequencePushConsumer = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/SequencePushConsumer:1.0', 'SequencePushConsumer')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/SequencePushConsumer:1.0'] = _0_CosNotifyComm._d_SequencePushConsumer
_0_CosNotifyComm.SequencePushConsumer = omniORB.newEmptyClass()

class SequencePushConsumer(_0_CosNotifyComm.NotifyPublish):
    _NP_RepositoryId = _0_CosNotifyComm._d_SequencePushConsumer[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.SequencePushConsumer = SequencePushConsumer
_0_CosNotifyComm._tc_SequencePushConsumer = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_SequencePushConsumer)
omniORB.registerType(SequencePushConsumer._NP_RepositoryId, _0_CosNotifyComm._d_SequencePushConsumer, _0_CosNotifyComm._tc_SequencePushConsumer)
SequencePushConsumer._d_push_structured_events = (
 (
  omniORB.typeMapping['IDL:omg.org/CosNotification/EventBatch:1.0'],), (), {_0_CosEventComm.Disconnected._NP_RepositoryId: _0_CosEventComm._d_Disconnected})
SequencePushConsumer._d_disconnect_sequence_push_consumer = ((), (), None)

class _objref_SequencePushConsumer(_0_CosNotifyComm._objref_NotifyPublish):
    _NP_RepositoryId = SequencePushConsumer._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifyPublish.__init__(self, obj)

    def push_structured_events(self, *args):
        return self._obj.invoke('push_structured_events', _0_CosNotifyComm.SequencePushConsumer._d_push_structured_events, args)

    def disconnect_sequence_push_consumer(self, *args):
        return self._obj.invoke('disconnect_sequence_push_consumer', _0_CosNotifyComm.SequencePushConsumer._d_disconnect_sequence_push_consumer, args)


omniORB.registerObjref(SequencePushConsumer._NP_RepositoryId, _objref_SequencePushConsumer)
_0_CosNotifyComm._objref_SequencePushConsumer = _objref_SequencePushConsumer
del SequencePushConsumer
del _objref_SequencePushConsumer
__name__ = 'CosNotifyComm__POA'

class SequencePushConsumer(_0_CosNotifyComm__POA.NotifyPublish):
    _NP_RepositoryId = _0_CosNotifyComm.SequencePushConsumer._NP_RepositoryId
    _omni_op_d = {'push_structured_events':_0_CosNotifyComm.SequencePushConsumer._d_push_structured_events, 
     'disconnect_sequence_push_consumer':_0_CosNotifyComm.SequencePushConsumer._d_disconnect_sequence_push_consumer}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifyPublish._omni_op_d)


SequencePushConsumer._omni_skeleton = SequencePushConsumer
_0_CosNotifyComm__POA.SequencePushConsumer = SequencePushConsumer
omniORB.registerSkeleton(SequencePushConsumer._NP_RepositoryId, SequencePushConsumer)
del SequencePushConsumer
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_SequencePullConsumer = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/SequencePullConsumer:1.0', 'SequencePullConsumer')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/SequencePullConsumer:1.0'] = _0_CosNotifyComm._d_SequencePullConsumer
_0_CosNotifyComm.SequencePullConsumer = omniORB.newEmptyClass()

class SequencePullConsumer(_0_CosNotifyComm.NotifyPublish):
    _NP_RepositoryId = _0_CosNotifyComm._d_SequencePullConsumer[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.SequencePullConsumer = SequencePullConsumer
_0_CosNotifyComm._tc_SequencePullConsumer = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_SequencePullConsumer)
omniORB.registerType(SequencePullConsumer._NP_RepositoryId, _0_CosNotifyComm._d_SequencePullConsumer, _0_CosNotifyComm._tc_SequencePullConsumer)
SequencePullConsumer._d_disconnect_sequence_pull_consumer = ((), (), None)

class _objref_SequencePullConsumer(_0_CosNotifyComm._objref_NotifyPublish):
    _NP_RepositoryId = SequencePullConsumer._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifyPublish.__init__(self, obj)

    def disconnect_sequence_pull_consumer(self, *args):
        return self._obj.invoke('disconnect_sequence_pull_consumer', _0_CosNotifyComm.SequencePullConsumer._d_disconnect_sequence_pull_consumer, args)


omniORB.registerObjref(SequencePullConsumer._NP_RepositoryId, _objref_SequencePullConsumer)
_0_CosNotifyComm._objref_SequencePullConsumer = _objref_SequencePullConsumer
del SequencePullConsumer
del _objref_SequencePullConsumer
__name__ = 'CosNotifyComm__POA'

class SequencePullConsumer(_0_CosNotifyComm__POA.NotifyPublish):
    _NP_RepositoryId = _0_CosNotifyComm.SequencePullConsumer._NP_RepositoryId
    _omni_op_d = {'disconnect_sequence_pull_consumer': _0_CosNotifyComm.SequencePullConsumer._d_disconnect_sequence_pull_consumer}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifyPublish._omni_op_d)


SequencePullConsumer._omni_skeleton = SequencePullConsumer
_0_CosNotifyComm__POA.SequencePullConsumer = SequencePullConsumer
omniORB.registerSkeleton(SequencePullConsumer._NP_RepositoryId, SequencePullConsumer)
del SequencePullConsumer
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_SequencePullSupplier = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/SequencePullSupplier:1.0', 'SequencePullSupplier')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/SequencePullSupplier:1.0'] = _0_CosNotifyComm._d_SequencePullSupplier
_0_CosNotifyComm.SequencePullSupplier = omniORB.newEmptyClass()

class SequencePullSupplier(_0_CosNotifyComm.NotifySubscribe):
    _NP_RepositoryId = _0_CosNotifyComm._d_SequencePullSupplier[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.SequencePullSupplier = SequencePullSupplier
_0_CosNotifyComm._tc_SequencePullSupplier = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_SequencePullSupplier)
omniORB.registerType(SequencePullSupplier._NP_RepositoryId, _0_CosNotifyComm._d_SequencePullSupplier, _0_CosNotifyComm._tc_SequencePullSupplier)
SequencePullSupplier._d_pull_structured_events = (
 (
  omniORB.tcInternal.tv_long,), (omniORB.typeMapping['IDL:omg.org/CosNotification/EventBatch:1.0'],), {_0_CosEventComm.Disconnected._NP_RepositoryId: _0_CosEventComm._d_Disconnected})
SequencePullSupplier._d_try_pull_structured_events = ((omniORB.tcInternal.tv_long,), (omniORB.typeMapping['IDL:omg.org/CosNotification/EventBatch:1.0'], omniORB.tcInternal.tv_boolean), {_0_CosEventComm.Disconnected._NP_RepositoryId: _0_CosEventComm._d_Disconnected})
SequencePullSupplier._d_disconnect_sequence_pull_supplier = ((), (), None)

class _objref_SequencePullSupplier(_0_CosNotifyComm._objref_NotifySubscribe):
    _NP_RepositoryId = SequencePullSupplier._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifySubscribe.__init__(self, obj)

    def pull_structured_events(self, *args):
        return self._obj.invoke('pull_structured_events', _0_CosNotifyComm.SequencePullSupplier._d_pull_structured_events, args)

    def try_pull_structured_events(self, *args):
        return self._obj.invoke('try_pull_structured_events', _0_CosNotifyComm.SequencePullSupplier._d_try_pull_structured_events, args)

    def disconnect_sequence_pull_supplier(self, *args):
        return self._obj.invoke('disconnect_sequence_pull_supplier', _0_CosNotifyComm.SequencePullSupplier._d_disconnect_sequence_pull_supplier, args)


omniORB.registerObjref(SequencePullSupplier._NP_RepositoryId, _objref_SequencePullSupplier)
_0_CosNotifyComm._objref_SequencePullSupplier = _objref_SequencePullSupplier
del SequencePullSupplier
del _objref_SequencePullSupplier
__name__ = 'CosNotifyComm__POA'

class SequencePullSupplier(_0_CosNotifyComm__POA.NotifySubscribe):
    _NP_RepositoryId = _0_CosNotifyComm.SequencePullSupplier._NP_RepositoryId
    _omni_op_d = {'pull_structured_events':_0_CosNotifyComm.SequencePullSupplier._d_pull_structured_events, 
     'try_pull_structured_events':_0_CosNotifyComm.SequencePullSupplier._d_try_pull_structured_events,  'disconnect_sequence_pull_supplier':_0_CosNotifyComm.SequencePullSupplier._d_disconnect_sequence_pull_supplier}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifySubscribe._omni_op_d)


SequencePullSupplier._omni_skeleton = SequencePullSupplier
_0_CosNotifyComm__POA.SequencePullSupplier = SequencePullSupplier
omniORB.registerSkeleton(SequencePullSupplier._NP_RepositoryId, SequencePullSupplier)
del SequencePullSupplier
__name__ = 'CosNotifyComm'
_0_CosNotifyComm._d_SequencePushSupplier = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosNotifyComm/SequencePushSupplier:1.0', 'SequencePushSupplier')
omniORB.typeMapping['IDL:omg.org/CosNotifyComm/SequencePushSupplier:1.0'] = _0_CosNotifyComm._d_SequencePushSupplier
_0_CosNotifyComm.SequencePushSupplier = omniORB.newEmptyClass()

class SequencePushSupplier(_0_CosNotifyComm.NotifySubscribe):
    _NP_RepositoryId = _0_CosNotifyComm._d_SequencePushSupplier[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_CosNotifyComm.SequencePushSupplier = SequencePushSupplier
_0_CosNotifyComm._tc_SequencePushSupplier = omniORB.tcInternal.createTypeCode(_0_CosNotifyComm._d_SequencePushSupplier)
omniORB.registerType(SequencePushSupplier._NP_RepositoryId, _0_CosNotifyComm._d_SequencePushSupplier, _0_CosNotifyComm._tc_SequencePushSupplier)
SequencePushSupplier._d_disconnect_sequence_push_supplier = ((), (), None)

class _objref_SequencePushSupplier(_0_CosNotifyComm._objref_NotifySubscribe):
    _NP_RepositoryId = SequencePushSupplier._NP_RepositoryId

    def __init__(self, obj):
        _0_CosNotifyComm._objref_NotifySubscribe.__init__(self, obj)

    def disconnect_sequence_push_supplier(self, *args):
        return self._obj.invoke('disconnect_sequence_push_supplier', _0_CosNotifyComm.SequencePushSupplier._d_disconnect_sequence_push_supplier, args)


omniORB.registerObjref(SequencePushSupplier._NP_RepositoryId, _objref_SequencePushSupplier)
_0_CosNotifyComm._objref_SequencePushSupplier = _objref_SequencePushSupplier
del SequencePushSupplier
del _objref_SequencePushSupplier
__name__ = 'CosNotifyComm__POA'

class SequencePushSupplier(_0_CosNotifyComm__POA.NotifySubscribe):
    _NP_RepositoryId = _0_CosNotifyComm.SequencePushSupplier._NP_RepositoryId
    _omni_op_d = {'disconnect_sequence_push_supplier': _0_CosNotifyComm.SequencePushSupplier._d_disconnect_sequence_push_supplier}
    _omni_op_d.update(_0_CosNotifyComm__POA.NotifySubscribe._omni_op_d)


SequencePushSupplier._omni_skeleton = SequencePushSupplier
_0_CosNotifyComm__POA.SequencePushSupplier = SequencePushSupplier
omniORB.registerSkeleton(SequencePushSupplier._NP_RepositoryId, SequencePushSupplier)
del SequencePushSupplier
__name__ = 'CosNotifyComm'
__name__ = 'CosNotifyComm_idl'
_exported_modules = ('CosNotifyComm', )