# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/netsoul/tools.py
# Compiled at: 2013-09-10 02:43:40
import re, string

def urlEncode(s):
    r = ''
    if not isinstance(s, unicode):
        s = unicode(s, 'utf8')
    for c in s:
        if c not in string.ascii_letters + string.digits:
            o = ord(c)
            r += ('%%0%s' if o < 16 else '%%%s') % hex(o).upper()[2:]
        else:
            r += c

    return r


def urlDecode(s):
    r = ''
    if not isinstance(s, unicode):
        s = unicode(s, 'utf8')
    while s:
        if s[0] == '%':
            try:
                r += unichr(int(s[1:3], 16))
            except ValueError:
                r += '?'

            s = s[3:]
        else:
            r += s[0]
            s = s[1:]

    return r


class Rea(object):

    def __init__(self, regex, f):
        self._regex = re.compile(regex)
        self._f = f

    def try_call(self, entry):
        m = self._regex.match(entry)
        if m is not None and self._f is not None:
            self._f(**m.groupdict())
            return True
        else:
            return False

    def try_call_cmd(self, entry, info):
        m = self._regex.match(entry)
        if m is not None and self._f is not None:
            self._f(info, **m.groupdict())
            return True
        else:
            return False


class ReaList(object):

    def __init__(self, *args):
        self._reas = [ rea for rea in args if isinstance(rea, Rea) ]

    def found_match(self, entry):
        for m in self._reas:
            if m.try_call(entry):
                return True

        return False

    def found_match_cmd(self, entry, info):
        for m in self._reas:
            if m.try_call_cmd(entry, info):
                return True

        return False


class NsUserCmdInfo(object):

    def __init__(self, no, login, ip, location):
        self._no, self._login, self._ip, self._location = (
         int(no), login, ip, location)

    def __str__(self):
        return '<%d %s@%s "%s">' % (self.no, self.login, self.ip, self.location)

    @property
    def no(self):
        return self._no

    @property
    def login(self):
        return self._login

    @property
    def ip(self):
        return self._ip

    @property
    def location(self):
        return self._location


class NsWhoEntry(object):

    def __init__(self, no, login, ip, location, state, res):
        self._no, self._login, self._ip, self._location, self._state, self._res = (
         int(no), login, ip, location, state, res)

    @property
    def no(self):
        return self._no

    @property
    def login(self):
        return self._login

    @property
    def ip(self):
        return self._ip

    @property
    def location(self):
        return self._location

    @property
    def state(self):
        return self._state

    @property
    def res(self):
        return self._res

    def __repr__(self):
        return '<NsWhoEntry %d %s %s %s %s %s>' % (self.no, self.login, self.ip, self.location, self.state, self.res)


class NsWhoResult(object):

    def __init__(self, logins):
        self._logins, self._list = logins, []

    @property
    def logins(self):
        return self._logins

    def add(self, entry):
        self._list.append(entry)

    def __iter__(self):
        return iter(self._list)

    def __repr__(self):
        return '<NsWhoResult %r>' % self._list