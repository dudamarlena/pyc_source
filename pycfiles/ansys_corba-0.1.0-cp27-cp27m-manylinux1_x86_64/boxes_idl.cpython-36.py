# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./boxes_idl.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 2017 bytes
import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA
_omnipy.checkVersion(4, 2, __file__, 1)
try:
    property
except NameError:

    def property(*args):
        pass


__name__ = 'CORBA'
_0_CORBA = omniORB.openModule('CORBA', '/tmp/corba/omni/share/idl/omniORB/boxes.idl')
_0_CORBA__POA = omniORB.openModule('CORBA__POA', '/tmp/corba/omni/share/idl/omniORB/boxes.idl')

class StringValue:
    _NP_RepositoryId = 'IDL:omg.org/CORBA/StringValue:1.0'

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')


_0_CORBA.StringValue = StringValue
_0_CORBA._d_StringValue = (omniORB.tcInternal.tv_value_box, StringValue, StringValue._NP_RepositoryId, 'StringValue', (omniORB.tcInternal.tv_string, 0))
_0_CORBA._tc_StringValue = omniORB.tcInternal.createTypeCode(_0_CORBA._d_StringValue)
omniORB.registerType(StringValue._NP_RepositoryId, _0_CORBA._d_StringValue, _0_CORBA._tc_StringValue)
omniORB.registerValueFactory(StringValue._NP_RepositoryId, StringValue)
del StringValue

class WStringValue:
    _NP_RepositoryId = 'IDL:omg.org/CORBA/WStringValue:1.0'

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')


_0_CORBA.WStringValue = WStringValue
_0_CORBA._d_WStringValue = (omniORB.tcInternal.tv_value_box, WStringValue, WStringValue._NP_RepositoryId, 'WStringValue', (omniORB.tcInternal.tv_wstring, 0))
_0_CORBA._tc_WStringValue = omniORB.tcInternal.createTypeCode(_0_CORBA._d_WStringValue)
omniORB.registerType(WStringValue._NP_RepositoryId, _0_CORBA._d_WStringValue, _0_CORBA._tc_WStringValue)
omniORB.registerValueFactory(WStringValue._NP_RepositoryId, WStringValue)
del WStringValue
__name__ = 'boxes_idl'
_exported_modules = ('CORBA', )