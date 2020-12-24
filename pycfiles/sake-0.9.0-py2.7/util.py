# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sake\util.py
# Compiled at: 2011-03-08 02:45:31
"""Utility module
"""
import codecs, ConfigParser, functools, sys, time, os, stackless
from . import const
from .errors import AccessError
ConfigParser.open = functools.partial(codecs.open, encoding='utf-8')
ConfigParser.str = unicode

def strx(o):
    """strx(o) -> string
    Works like str(o) but catches unicode errors and converts gracefully to strings.
    """
    try:
        return str(o)
    except UnicodeEncodeError:
        return unicode(o).encode('ascii', 'replace')


if sys.platform == 'win32':
    GetTime = time.clock
else:
    GetTime = time.time
clockStart = GetTime()

class Bunch(dict):
    """"""
    __slots__ = []

    def __repr__(self):
        return 'Bunch of %s' % dict.__repr__(self)

    def __getattr__(self, key):
        try:
            return super(Bunch, self).__getitem__(key)
        except KeyError:
            raise AttributeError(key)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getstate__(self):
        pass

    def Copy(self):
        return Bunch(self.copy())


def GetSession():
    """Returns the current active session"""
    t = stackless.getcurrent()
    return getattr(t, 'session', None)


def HasAccess(role, session=None):
    """Does role check on the current active session"""
    if session is None:
        session = GetSession()
    if session.role == const.ROLE_SERVICE:
        return True
    else:
        if session.role == const.ROLE_ADMIN and role in (const.ROLE_USER,):
            return True
        else:
            return session.role & role == role

        return


def VerifyAccess(role, context='Object'):
    """Same as HasAccess, but raises an exception instead of returning False"""
    if not HasAccess(role):
        s = GetSession()
        msg = "Access denied. '%s' requires role %s, but %s has %s."
        args = (context, FormatRole(role), s, FormatRole(s.role))
        raise AccessError(msg % args)


def FormatRole(role):
    """A hack method to stringify role id's"""
    if role == const.ROLE_NOACCESS:
        return 'ROLE_NOACCESS'
    else:
        roles = dict([ (k, v) for k, v in const.__dict__.items() if k.startswith('ROLE_') and k != 'ROLE_ANY' ])
        format = ''
        for rolename, flag in roles.iteritems():
            if flag & role == flag:
                format += '%s|' % rolename

        if format:
            return format[:-1]
        return str(role)


def ReportLoadedModules():
    mods = []
    for module in sys.modules.values():
        if module and hasattr(module, '__file__'):
            path = os.path.abspath(os.path.join(os.getcwd(), module.__file__))
            mods.append(path)

    mods.sort()
    f = open('loadedModules.txt', 'w')
    for path in mods:
        f.write('%s\r\n' % path)

    f.close()
    sys.exit('Report of loaded modules created.')


def GetAppTitle(appname):
    """Returns a decorated 'appname' title, including version, rank, pid and so forth."""
    import __main__
    file = getattr(__main__, '__file__', 'no file')
    title = '%s from %s (pid=%s)' % (appname, os.path.split(file)[(-1)], os.getpid())
    return title


def enum(*sequential, **named):
    """
    Automatic enumeration type creation
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('enum', (), enums)