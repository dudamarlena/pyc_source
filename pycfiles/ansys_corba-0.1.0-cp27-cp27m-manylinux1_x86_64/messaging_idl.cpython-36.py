# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./messaging_idl.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 4284 bytes
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
import pollable_idl
_0_CORBA = omniORB.openModule('CORBA')
_0_CORBA__POA = omniORB.openModule('CORBA__POA')
__name__ = 'Messaging'
_0_Messaging = omniORB.openModule('Messaging', '/tmp/corba/omni/share/idl/omniORB/messaging.idl')
_0_Messaging__POA = omniORB.openModule('Messaging__POA', '/tmp/corba/omni/share/idl/omniORB/messaging.idl')
_0_Messaging._d_ReplyHandler = (
 omniORB.tcInternal.tv_objref, 'IDL:omg.org/Messaging/ReplyHandler:1.0', 'ReplyHandler')
omniORB.typeMapping['IDL:omg.org/Messaging/ReplyHandler:1.0'] = _0_Messaging._d_ReplyHandler
_0_Messaging.ReplyHandler = omniORB.newEmptyClass()

class ReplyHandler:
    _NP_RepositoryId = _0_Messaging._d_ReplyHandler[1]

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil


_0_Messaging.ReplyHandler = ReplyHandler
_0_Messaging._tc_ReplyHandler = omniORB.tcInternal.createTypeCode(_0_Messaging._d_ReplyHandler)
omniORB.registerType(ReplyHandler._NP_RepositoryId, _0_Messaging._d_ReplyHandler, _0_Messaging._tc_ReplyHandler)

class _objref_ReplyHandler(CORBA.Object):
    _NP_RepositoryId = ReplyHandler._NP_RepositoryId

    def __init__(self, obj):
        CORBA.Object.__init__(self, obj)


omniORB.registerObjref(ReplyHandler._NP_RepositoryId, _objref_ReplyHandler)
_0_Messaging._objref_ReplyHandler = _objref_ReplyHandler
del ReplyHandler
del _objref_ReplyHandler
__name__ = 'Messaging__POA'

class ReplyHandler(PortableServer.Servant):
    _NP_RepositoryId = _0_Messaging.ReplyHandler._NP_RepositoryId
    _omni_op_d = {}


ReplyHandler._omni_skeleton = ReplyHandler
_0_Messaging__POA.ReplyHandler = ReplyHandler
omniORB.registerSkeleton(ReplyHandler._NP_RepositoryId, ReplyHandler)
del ReplyHandler
__name__ = 'Messaging'

class Poller(_0_CORBA.Pollable):
    _NP_RepositoryId = 'IDL:omg.org/Messaging/Poller:1.0'

    def __init__(self, *args, **kwargs):
        raise RuntimeError('Cannot construct objects of this type.')


_0_Messaging.Poller = Poller
_0_Messaging._d_Poller = (omniORB.tcInternal.tv_value, Poller, Poller._NP_RepositoryId, 'Poller', _0_CORBA.VM_ABSTRACT, None, _0_CORBA.tcInternal.tv_null)
_0_Messaging._tc_Poller = omniORB.tcInternal.createTypeCode(_0_Messaging._d_Poller)
omniORB.registerType(Poller._NP_RepositoryId, _0_Messaging._d_Poller, _0_Messaging._tc_Poller)
del Poller
_0_Messaging._d_ExceptionHolder = (
 omniORB.tcInternal.tv__indirect, ['IDL:omg.org/Messaging/ExceptionHolder:1.0'])
omniORB.typeMapping['IDL:omg.org/Messaging/ExceptionHolder:1.0'] = _0_Messaging._d_ExceptionHolder
_0_Messaging.ExceptionHolder = omniORB.newEmptyClass()

class ExceptionHolder(_0_CORBA.ValueBase):
    _NP_RepositoryId = 'IDL:omg.org/Messaging/ExceptionHolder:1.0'

    def __init__(self, *args, **kwargs):
        if args:
            if len(args) != 0:
                raise TypeError('ExceptionHolder() takes 0 arguments (%d given)' % len(args))
        if kwargs:
            self.__dict__.update(kwargs)


_0_Messaging.ExceptionHolder = ExceptionHolder
_0_Messaging._d_ExceptionHolder = (omniORB.tcInternal.tv_value, ExceptionHolder, ExceptionHolder._NP_RepositoryId, 'ExceptionHolder', _0_CORBA.VM_NONE, None, _0_CORBA.tcInternal.tv_null)
_0_Messaging._tc_ExceptionHolder = omniORB.tcInternal.createTypeCode(_0_Messaging._d_ExceptionHolder)
omniORB.registerType(ExceptionHolder._NP_RepositoryId, _0_Messaging._d_ExceptionHolder, _0_Messaging._tc_ExceptionHolder)
del ExceptionHolder
__name__ = 'messaging_idl'
_exported_modules = ('Messaging', )