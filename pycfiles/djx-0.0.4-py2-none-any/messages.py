# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/checks/messages.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.utils.encoding import force_str, python_2_unicode_compatible
DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50

@python_2_unicode_compatible
class CheckMessage(object):

    def __init__(self, level, msg, hint=None, obj=None, id=None):
        assert isinstance(level, int), b'The first argument should be level.'
        self.level = level
        self.msg = msg
        self.hint = hint
        self.obj = obj
        self.id = id

    def __eq__(self, other):
        return isinstance(other, self.__class__) and all(getattr(self, attr) == getattr(other, attr) for attr in [b'level', b'msg', b'hint', b'obj', b'id'])

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        from django.db import models
        if self.obj is None:
            obj = b'?'
        elif isinstance(self.obj, models.base.ModelBase):
            obj = self.obj._meta.label
        else:
            obj = force_str(self.obj)
        id = b'(%s) ' % self.id if self.id else b''
        hint = b'\n\tHINT: %s' % self.hint if self.hint else b''
        return b'%s: %s%s%s' % (obj, id, self.msg, hint)

    def __repr__(self):
        return b'<%s: level=%r, msg=%r, hint=%r, obj=%r, id=%r>' % (
         self.__class__.__name__, self.level, self.msg, self.hint, self.obj, self.id)

    def is_serious(self, level=ERROR):
        return self.level >= level

    def is_silenced(self):
        from django.conf import settings
        return self.id in settings.SILENCED_SYSTEM_CHECKS


class Debug(CheckMessage):

    def __init__(self, *args, **kwargs):
        super(Debug, self).__init__(DEBUG, *args, **kwargs)


class Info(CheckMessage):

    def __init__(self, *args, **kwargs):
        super(Info, self).__init__(INFO, *args, **kwargs)


class Warning(CheckMessage):

    def __init__(self, *args, **kwargs):
        super(Warning, self).__init__(WARNING, *args, **kwargs)


class Error(CheckMessage):

    def __init__(self, *args, **kwargs):
        super(Error, self).__init__(ERROR, *args, **kwargs)


class Critical(CheckMessage):

    def __init__(self, *args, **kwargs):
        super(Critical, self).__init__(CRITICAL, *args, **kwargs)