# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/moyaexceptions.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from .compat import implements_to_string
from . import diagnose
from .interface import AttributeExposer
__all__ = [
 b'MoyaException',
 b'FatalMoyaException',
 b'throw']

@implements_to_string
class MoyaException(Exception, AttributeExposer):
    fatal = False
    __moya_exposed_attributes__ = [
     b'type', b'msg', b'info', b'diagnosis']

    def __init__(self, type, msg, diagnosis=None, info=None):
        self.type = type
        self.msg = msg
        self._diagnosis = diagnosis
        self.info = info or {}

    @property
    def diagnosis(self):
        return self._diagnosis or diagnose.diagnose_moya_exception(self)

    def __str__(self):
        return (b'{}: {}').format(self.type, self.msg)

    def __repr__(self):
        return b'<exception %s:"%s">' % (self.type, self.msg)

    def __moyaconsole__(self, console):
        from . import pilot
        console(self.type + b': ', fg=b'red', bold=True)(self.msg).nl()
        if self.info:
            console.obj(pilot.context, self.info)


class FatalMoyaException(MoyaException):
    fatal = True


def throw(type, msg, diagnosis=None, info=None):
    raise MoyaException(type, msg, diagnosis=diagnosis, info=info)