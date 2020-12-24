# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/flask_boot/project/application/exception/util.py
# Compiled at: 2018-08-07 11:02:04
from __future__ import absolute_import, division, unicode_literals
from . import SysExc, UserExc, DevExc
from .error_code import CODE_MSG, DEV_EXCEPTION_UNDEFINED_ERROR

def gen_exception_raiser(exc_cls):

    def wrapper(error_code, *args, **kwargs):
        msg = CODE_MSG.get(error_code)
        if not msg:
            raise DevExc(error_code, CODE_MSG[DEV_EXCEPTION_UNDEFINED_ERROR])
        origin_exc = kwargs.pop(b'exc', None)
        if origin_exc:
            msg += (b',{exc!s}').format(exc=origin_exc)
        if args:
            raise exc_cls(error_code, msg.format(*args))
        elif kwargs:
            raise exc_cls(error_code, msg.format(**kwargs))
        raise exc_cls(error_code, msg)
        return

    return wrapper


raise_server_exc = gen_exception_raiser(SysExc)
raise_user_exc = gen_exception_raiser(UserExc)
raise_dev_exc = gen_exception_raiser(DevExc)