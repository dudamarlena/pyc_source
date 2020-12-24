# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/uamd/device/mobile.py
# Compiled at: 2011-11-22 04:04:45
from . import Device
import re

class Mobile(Device):
    """
    The base class of mobile device
    """
    _carrier = None
    _encoding = None

    def __init__(self, name=None, support_cookie=None, uid=None):
        """Constructor of the class

        :param string name:         the name of device. it is also stored in ``model`` property
        :param bool support_cookie: whether the device support cookie
        :param string uid:          the carrier's UID
        """
        super(Mobile, self).__init__(name, support_cookie)
        self._uid = uid
        self._model = name

    def __unicode__(self):
        return '%s %s' % (self.carrier, self.name)

    carrier = property(lambda self: self._carrier)
    encoding = property(lambda self: self._encoding)
    uid = property(lambda self: self._uid)
    model = property(lambda self: self._model)


class DoCoMo(Mobile):
    _carrier = 'docomo'
    _encoding = 'cp932'
    _pattern = re.compile('DoCoMo/(?P<type>[12].0)[ \\/]')
    _pattern_mova = re.compile('DoCoMo/1.0/(?P<name>[^/]*)(?:/c(?P<cache>\\d*)|)')
    _pattern_foma = re.compile('DoCoMo/2.0 (?P<name>[^\\(]*)\\(c(?P<cache>\\d*)')

    def __init__(self, type, name=None, support_cookie=None, uid=None):
        super(DoCoMo, self).__init__(name, support_cookie, uid)
        self._type = type

    type = property(lambda self: self._type)

    def _parse_mova(cls, ua):
        m = cls._pattern_mova.match(ua)
        name, cache = m.groups()
        cache = int(cache) if cache else 5
        return (name, cache)

    _parse_mova = classmethod(_parse_mova)

    def _parse_foma(cls, ua):
        m = cls._pattern_foma.match(ua)
        name, cache = m.groups()
        cache = int(cache)
        return (name, cache)

    _parse_foma = classmethod(_parse_foma)

    def factory(cls, meta):
        uid = meta.get('HTTP_X_DCMGUID', None)
        ua = meta.get('HTTP_USER_AGENT', None)
        if cls._pattern_mova.match(ua):
            name, cache = cls._parse_mova(ua)
            type = 'MOVA'
        elif cls._pattern_foma.match(ua):
            name, cache = cls._parse_foma(ua)
            type = 'FOMA'
        else:
            raise NotImplementedError('unknown user agent for DoCoMo (%s)' % ua)
        support_cookie = cache >= 500
        return cls(type, name, support_cookie, uid)

    factory = classmethod(factory)


class KDDI(Mobile):
    _carrier = 'kddi'
    _encoding = 'cp932'
    _pattern = re.compile('(?:(?:KDDI-)|(?:SIE-))(?P<name>[^\\s/]*)')

    def __init__(self, hdml, name=None, support_cookie=None, uid=None):
        super(KDDI, self).__init__(name, support_cookie, uid)
        self._hdml = hdml

    hdml = property(lambda self: self._hdml)

    def factory(cls, meta):
        uid = meta.get('HTTP_X_UP_SUBNO', None)
        ua = meta.get('HTTP_USER_AGENT', None)
        m = cls._pattern.match(ua)
        name = m.group('name')
        support_cookie = True
        hdml = ua.startswith('SIE')
        return cls(hdml, name, support_cookie, uid)

    factory = classmethod(factory)


class SoftBank(Mobile):
    _carrier = 'softbank'
    _encoding = 'utf8'
    _pattern = re.compile('(?P<type>J-PHONE|Vodafone|SoftBank)/(?P<version>[\\d\\.]*)/(?P<name>[^/\\[]*)')

    def __init__(self, type, name=None, support_cookie=None, uid=None):
        super(SoftBank, self).__init__(name, support_cookie, uid)
        self._type = type

    type = property(lambda self: self._type)

    def factory(cls, meta):
        uid = meta.get('HTTP_X_JPHONE_UID', None)
        ua = meta.get('HTTP_USER_AGENT', None)
        m = cls._pattern.match(ua)
        type, version, name = m.groups()
        if type == 'J-PHONE':
            support_cookie = version.startswith('5')
        else:
            support_cookie = True
        return cls(type, name, support_cookie, uid)

    factory = classmethod(factory)


devices = (
 DoCoMo, KDDI, SoftBank)