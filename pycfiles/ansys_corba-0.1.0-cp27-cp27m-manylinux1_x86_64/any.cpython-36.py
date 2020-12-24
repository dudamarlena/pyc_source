# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./any.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 11943 bytes
"""
omniORB.any module -- Any support functions.

to_any(data)                  -- try to coerce data to an Any.

from_any(any, keep_structs=0) -- return any's contents as plain Python
                                 objects. If keep_structs is true,
                                 CORBA structs are kept as Python class
                                 instances; if false, they are expanded
                                 to dictionaries.
"""
import omniORB
from . import CORBA, tcInternal
import random, threading
__all__ = [
 'to_any', 'from_any']
random.seed()
_idbase = '%08x' % random.randrange(0, 2147483647)
_idcount = 0
_idlock = threading.Lock()
INVALID_MEMBER_KINDS = [
 tcInternal.tv_null,
 tcInternal.tv_void,
 tcInternal.tv_except]
_f = CORBA.fixed(0)
FixedType = type(_f)
try:
    if bytes is str:
        raise NameError()
except NameError:

    class bytes(object):
        pass


def to_any(data):
    """to_any(data) -- try to return data as a CORBA.Any"""
    tc, val = _to_tc_value(data)
    return CORBA.Any(tc, val)


def _to_tc_value(data):
    """_to_tc_value(data) -- return TypeCode and value for Any insertion"""
    global _idcount
    if data is None:
        return (
         CORBA.TC_null, None)
    elif isinstance(data, str):
        return (
         CORBA.TC_string, data)
    else:
        if isinstance(data, str):
            return (
             CORBA.TC_wstring, data)
        else:
            if isinstance(data, bytes):
                return (
                 CORBA._tc_OctetSeq, data)
            if isinstance(data, bool):
                return (
                 CORBA.TC_boolean, data)
        if isinstance(data, int):
            if -2147483648 <= data <= 2147483647:
                return (
                 CORBA.TC_long, int(data))
            else:
                if 0 <= data <= 4294967295:
                    return (CORBA.TC_ulong, data)
                if -9223372036854775808 <= data <= 9223372036854775807:
                    return (
                     CORBA.TC_longlong, data)
                if 0 <= data <= 18446744073709551615:
                    return (
                     CORBA.TC_ulonglong, data)
            raise CORBA.BAD_PARAM(omniORB.BAD_PARAM_PythonValueOutOfRange, CORBA.COMPLETED_NO)
        else:
            if isinstance(data, float):
                return (
                 CORBA.TC_double, data)
            else:
                if isinstance(data, list):
                    if data == []:
                        tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                         tcInternal.tv_any, 0))
                        return (tc, data)
                    d0 = data[0]
                    if isinstance(d0, str):
                        for d in data:
                            if not isinstance(d, str):
                                break
                        else:
                            tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                             CORBA.TC_string._d, 0))
                            return (tc, data)

                    else:
                        if isinstance(d0, str):
                            for d in data:
                                if not isinstance(d, str):
                                    break
                            else:
                                tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                                 CORBA.TC_wstring._d, 0))
                                return (tc, data)

                        else:
                            if isinstance(d0, bytes):
                                for d in data:
                                    if not isinstance(d, bytes):
                                        break
                                else:
                                    tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                                     CORBA._tc_OctetSeq, 0))
                                    return (tc, data)

                            else:
                                if isinstance(d0, bool):
                                    for d in data:
                                        if not isinstance(d, bool):
                                            break
                                    else:
                                        tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                                         tcInternal.tv_boolean, 0))
                                        return (tc, data)

                                else:
                                    if isinstance(d0, int):
                                        min_v = max_v = 0
                                        for d in data:
                                            if not (isinstance(d, int) or isinstance(d, bool)):
                                                break
                                            if d < min_v:
                                                min_v = d
                                            if d > max_v:
                                                max_v = d
                                        else:
                                            if min_v >= -2147483648:
                                                if max_v <= 2147483647:
                                                    tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                                                     tcInternal.tv_long, 0))
                                                    return (tc, list(map(int, data)))
                                                else:
                                                    if min_v >= 0:
                                                        if max_v <= 4294967295:
                                                            tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                                                             tcInternal.tv_ulong, 0))
                                                            return (
                                                             tc, list(map(int, data)))
                                                    if min_v >= -9223372036854775808:
                                                        if max_v <= 9223372036854775807:
                                                            tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                                                             tcInternal.tv_longlong, 0))
                                                            return (tc, list(map(int, data)))
                                            else:
                                                if min_v >= 0:
                                                    if max_v <= 18446744073709551615:
                                                        tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                                                         tcInternal.tv_ulonglong, 0))
                                                        return (tc, list(map(int, data)))
                                            raise CORBA.BAD_PARAM(omniORB.BAD_PARAM_PythonValueOutOfRange, CORBA.COMPLETED_NO)

                                    else:
                                        if isinstance(d0, float):
                                            for d in data:
                                                if not isinstance(d, float):
                                                    break
                                            else:
                                                tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                                                 tcInternal.tv_double, 0))
                                                return (tc, data)

                                        else:
                                            if isinstance(d0, CORBA.Any):
                                                for d in data:
                                                    if not isinstance(d, CORBA.Any):
                                                        break
                                                else:
                                                    tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                                                     tcInternal.tv_any, 0))
                                                    return (tc, data)

                        tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                         tcInternal.tv_any, 0))
                        any_list = list(map(to_any, data))
                        atc = any_list[0]._t
                        if atc._k._v not in INVALID_MEMBER_KINDS:
                            for a in any_list:
                                if not a._t.equivalent(atc):
                                    break
                            else:
                                tc = tcInternal.createTypeCode((tcInternal.tv_sequence,
                                 atc._d, 0))
                                for i in range(len(any_list)):
                                    any_list[i] = any_list[i]._v

                        return (
                         tc, any_list)
                    if isinstance(data, tuple):
                        return _to_tc_value(list(data))
                    if isinstance(data, dict):
                        _idlock.acquire()
                        try:
                            _idcount = _idcount + 1
                            id = 'omni:%s:%08x' % (_idbase, _idcount)
                        finally:
                            _idlock.release()

                        dl = [tcInternal.tv_struct, None, id, '']
                        ms = []
                        svals = []
                        items = list(data.items())
                        for k, v in items:
                            if not isinstance(k, str):
                                raise CORBA.BAD_PARAM(omniORB.BAD_PARAM_WrongPythonType, CORBA.COMPLETED_NO)
                            t, v = _to_tc_value(v)
                            if t._k._v in INVALID_MEMBER_KINDS:
                                v = CORBA.Any(t, v)
                                t = CORBA.TC_any
                            ms.append(k)
                            dl.append(k)
                            dl.append(t._d)
                            svals.append(v)

                        cls = omniORB.createUnknownStruct(id, ms)
                        dl[1] = cls
                        tc = tcInternal.createTypeCode(tuple(dl))
                        value = cls(*svals)
                        return (tc, value)
                else:
                    if isinstance(data, FixedType):
                        if data == CORBA.fixed(0):
                            tc = tcInternal.createTypeCode((tcInternal.tv_fixed, 1, 0))
                        else:
                            tc = tcInternal.createTypeCode((tcInternal.tv_fixed,
                             data.precision(), data.decimals()))
                        return (
                         tc, data)
                    if isinstance(data, CORBA.Any):
                        return (
                         data._t, data._v)
                if isinstance(data, omniORB.EnumItem):
                    return (
                     omniORB.findTypeCode(data._parent_id), data)
            if hasattr(data, '_NP_RepositoryId'):
                return (
                 omniORB.findTypeCode(data._NP_RepositoryId), data)
    raise CORBA.BAD_PARAM(omniORB.BAD_PARAM_WrongPythonType, CORBA.COMPLETED_NO)


def from_any(any, keep_structs=0):
    """from_any(any, keep_structs=0) -- extract the data from an Any.

    If keep_structs is true, CORBA structs are left as Python
    instances; if false, structs are turned into dictionaries with
    string keys.
    """
    if not isinstance(any, CORBA.Any):
        raise CORBA.BAD_PARAM(omniORB.BAD_PARAM_WrongPythonType, CORBA.COMPLETED_NO)
    return _from_desc_value(any._t._d, any._v, keep_structs)


def _from_desc_value(desc, value, keep_structs=0):
    """_from_desc_value(desc,val,keep_structs) -- de-Any value"""
    if type(desc) is int:
        if desc == tcInternal.tv_boolean:
            return bool(value)
        if desc != tcInternal.tv_any:
            return value
        k = desc
    else:
        k = desc[0]
    while k == tcInternal.tv_alias:
        desc = desc[3]
        if type(desc) is int:
            if desc == tcInternal.tv_boolean:
                return bool(value)
            if desc != tcInternal.tv_any:
                return value
            k = desc
        else:
            k = desc[0]

    if k == tcInternal.tv_any:
        return _from_desc_value(value._t._d, value._v, keep_structs)
    if k == tcInternal.tv_struct:
        if keep_structs:
            return value
        d = {}
        for i in range(4, len(desc), 2):
            sm = desc[i]
            sd = desc[(i + 1)]
            d[sm] = _from_desc_value(sd, getattr(value, sm), keep_structs)

        return d
    else:
        if k in [tcInternal.tv_sequence, tcInternal.tv_array]:
            sd = desc[1]
            if type(sd) is int:
                if sd != tcInternal.tv_any:
                    return value
            rl = []
            for i in value:
                rl.append(_from_desc_value(sd, i, keep_structs))

            return rl
        return value