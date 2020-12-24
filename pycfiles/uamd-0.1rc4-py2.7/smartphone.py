# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/uamd/device/smartphone.py
# Compiled at: 2011-11-22 04:04:45
from . import Device
from mobile import SoftBank
import re

class SmartPhone(Device):
    _support_flush = None

    def __init__(self, name=None, support_cookie=None, support_flush=None):
        super(SmartPhone, self).__init__(name, support_cookie)
        self._support_flush = support_flush if support_flush is not None else self._support_flush
        return

    support_flush = property(lambda self: self._support_flush)
    is_smartphone = property(lambda self: True)


class iPhone(SmartPhone):
    _name = 'iPhone'
    _support_cookie = True
    _support_flush = False
    _pattern = re.compile('Mozilla/[\\d\\.]* \\(iPhone; U; CPU (?:(?:iPhone OS (?P<version>[\\w_]*))|)')
    _carrier = SoftBank._carrier
    _encoding = 'utf8'

    def __init__(self, version):
        super(iPhone, self).__init__()
        self._version = version

    def __unicode__(self):
        return '%s %s' % (self.name, self.version)

    version = property(lambda self: self._version)
    carrier = property(lambda self: self._carrier)
    encoding = property(lambda self: self._encoding)

    def factory(cls, meta):
        ua = meta.get('HTTP_USER_AGENT', None)
        m = cls._pattern.match(ua)
        version = m.group('version') or '1_0'
        version = version.replace('_', '.')
        return cls(version)

    factory = classmethod(factory)


class iPodTouch(iPhone):
    _name = 'iPod Touch'
    _pattern = re.compile('Mozilla/[\\d\\.]* \\(iPod; U; CPU (?:(?:iPhone OS (?P<version>[\\w_]*))|)')
    _carrier = None


class iPad(iPhone):
    _name = 'iPad'
    _pattern = re.compile('Mozilla/[\\d\\.]*\\(iPad; U; CPU (?:(?:iPhone OS (?P<version>[\\w_]*))|)')


class Android(SmartPhone):
    _name = 'Android'
    _support_cookie = True
    _support_flush = True
    _pattern = re.compile('Mozilla/[\\d\\.]* \\(Linux; U; Android (?P<version>[^;]*);(?P<language>[^;]*);(?P<model>[^;\\)]*)')

    def __init__(self, version, model):
        super(Android, self).__init__()
        self._version = version
        self._model = model

    def __unicode__(self):
        return '%s %s (%s)' % (self.name, self.version, self.model)

    version = property(lambda self: self._version)
    model = property(lambda self: self._model)

    def factory(cls, meta):
        ua = meta.get('HTTP_USER_AGENT', None)
        m = cls._pattern.match(ua)
        version = m.group('version')
        language = m.group('language')
        model = m.group('model')
        return cls(version, model)

    factory = classmethod(factory)


devices = (
 iPhone, iPodTouch, iPad, Android)