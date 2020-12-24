# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/uamd/device/browser.py
# Compiled at: 2011-11-22 04:06:07
from . import Device
import re

class Browser(Device):
    _support_cookie = True

    def __init__(self, version, os, name=None, support_cookie=None):
        super(Browser, self).__init__(name, support_cookie)
        self._version = version
        self._os = os

    version = property(lambda self: self._version)
    os = property(lambda self: self._os)


class InternetExplorer(Browser):
    _name = 'Internet Explorer'
    _pattern = re.compile('Mozilla/[\\d\\.]* \\(compatible; MSIE (?P<version>[\\d\\.]*); (?P<os>[^;]*);')

    def factory(cls, meta):
        ua = meta.get('HTTP_USER_AGENT', None)
        m = cls._pattern.match(ua)
        version, os = m.groups()
        return cls(version, os)

    factory = classmethod(factory)


class GoogleChrome(Browser):
    _name = 'Google Chrome'
    _pattern = re.compile('Mozilla/[\\d\\.]* \\([^;]*; U; (?P<os>[^;]*); .*Chrome/(?P<version>[\\d\\.]*)')

    def factory(cls, meta):
        ua = meta.get('HTTP_USER_AGENT', None)
        m = cls._pattern.match(ua)
        os, version = m.groups()
        return cls(version, os)

    factory = classmethod(factory)


class Lunascape(Browser):
    _name = 'Lunascape'
    _pattern = re.compile('Mozilla/[\\d\\.]* \\(compatible; MSIE [\\d\\.]*; (?P<os>[^;]*); .*Lunascape (?P<version>[^\\)]*)\\)')

    def factory(cls, meta):
        ua = meta.get('HTTP_USER_AGENT', None)
        m = cls._pattern.match(ua)
        os, version = m.groups()
        return cls(version, os)

    factory = classmethod(factory)


class Firefox(Browser):
    _name = 'Firefox'
    _pattern = re.compile('Mozilla/[\\d\\.]* \\([^;]*; U; (?P<os>[^;]*); .*Firefox/(?P<version>[\\d\\.]*)')

    def factory(cls, meta):
        ua = meta.get('HTTP_USER_AGENT', None)
        m = cls._pattern.match(ua)
        os, version = m.groups()
        return cls(version, os)

    factory = classmethod(factory)


class Safari(Browser):
    _name = 'Firefox'
    _pattern = re.compile('Mozilla/[\\d\\.]* \\([^;]*; U; (?P<os>[^;]*); .*Version/(?P<version>[\\d\\.]*) Safari')

    def factory(cls, meta):
        ua = meta.get('HTTP_USER_AGENT', None)
        m = cls._pattern.match(ua)
        os, version = m.groups()
        return cls(version, os)

    factory = classmethod(factory)


class Opera(Browser):
    _name = 'Opera'
    _pattern = None
    _pattern_s = re.compile('Opera/(?P<version>[\\d\\.]*) \\((?P<os>[^;]*);')
    _pattern_l = re.compile('Mozilla/[\\d\\.]* \\([^;]*; [^;]*; (?P<os>[^;]*); .*Opera (?P<version>[\\d\\.]*)')

    def fastcheck(cls, meta):
        ua = meta.get('HTTP_USER_AGENT', None)
        if ua:
            return 'Opera' in ua
        else:
            return False

    fastcheck = classmethod(fastcheck)

    def factory(cls, meta):
        ua = meta.get('HTTP_USER_AGENT', None)
        if cls._pattern_s.match(ua):
            m = cls._pattern_s.match(ua)
            version, os = m.groups()
        elif cls._pattern_l.match(ua):
            m = cls._pattern_l.match(ua)
            os, version = m.groups()
        else:
            raise NotImplementedError('unknown Opera user agent (%s)' % ua)
        return cls(version, os)

    factory = classmethod(factory)


devices = (
 Firefox, GoogleChrome, Lunascape, Safari, Opera, InternetExplorer)