# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/nlapi.py
# Compiled at: 2011-02-04 15:16:28
"""
NetLogger instrumentation API for Python

Write NetLogger log messages. Most users of this API will
use the Log class, which is a little like a 'Logger' object in the
Python logging API.

Utility functions include functions to get and set the Grid Job ID.
"""
__author__ = 'Dan Gunter'
__created__ = '1 April 2004'
__rcsid__ = '$Id: nlapi.py 27037 2011-02-04 20:16:27Z dang $'
import calendar, datetime, math, os, socket, string, sys, time, types, urlparse
from netlogger.nldate import utcFormatISO
from netlogger.util import uuid1

class ParseException(Exception):
    pass


class FormatException(Exception):
    pass


GID_ENV = 'NETLOGGER_GUID'
NLDEST_ENV = 'NL_DEST'
CFG_ENV = 'NL_CFG'
FIELD_SEP = ' '
REC_SEP = '\n'
EOR = '\n'
KEYVAL_SEP = '='
DEFAULT_PORT = 14380

class Level:
    NOLOG = 0
    FATAL = 1
    ERROR = 2
    WARN = 3
    WARNING = 3
    INFO = 4
    DEBUG = 5
    DEBUG1 = 6
    DEBUG2 = 7
    DEBUG3 = 8
    TRACE = DEBUG1
    ALL = -1
    names = {NOLOG: 'NOLOG', FATAL: 'Fatal', 
       ERROR: 'Error', 
       WARN: 'Warn', 
       INFO: 'Info', 
       DEBUG: 'Debug', 
       TRACE: 'Trace', 
       DEBUG2: 'Debug2', 
       DEBUG3: 'Debug3'}

    @staticmethod
    def getName(level):
        return Level.names.get(level, 'User')

    @staticmethod
    def getLevel(name):
        if name.isupper() and hasattr(Level, name):
            return getattr(Level, name)
        raise ValueError('no such level name: %s' % name)


DATE_FMT = '%04d-%02d-%02dT%02d:%02d:%02d'
TS_FIELD = 'ts'
EVENT_FIELD = 'event'
LEVEL_FIELD = 'level'
STATUS_FIELD = 'status'
MESSAGE_FIELD = 'msg'
HASH_FIELD = 'nlhash'

def quotestr(v):
    """Quote a string value to be output.
    """
    if not v:
        v = '""'
    elif ' ' in v or '\t' in v or '"' in v or '=' in v:
        v = '"%s"' % v.replace('"', '\\"')
    return v


def getGuid(create=True, env=GID_ENV):
    """Return a GUID.
    If 'create' is True (the default), and if none is found 
    in the environment then create one.
    """
    gid = os.environ.get(env, None)
    if gid is None:
        if create:
            gid = uuid1()
    return gid


def setGuid(id, env=GID_ENV):
    """Replace current guid in the environment with provided value.
    Return old value, or None if there was no old value.

    Note: may cause memory leak on FreeBSD and MacOS. See system docs.
    """
    old_gid = os.environ.get(env, None)
    os.environ[env] = id
    return old_gid


def clearGuid(env=GID_ENV):
    """Unset guid
    """
    old_gid = os.environ.get(env, None)
    if old_gid:
        del os.environ[env]
    return old_gid


_g_hostip = None

def getHost():
    global _g_hostip
    if _g_hostip is not None:
        return _g_hostip
    else:
        try:
            ip = socket.gethostbyname(socket.getfqdn())
        except:
            ip = '127.0.0.1'

        _g_hostip = ip
        return ip


def getProg():
    import sys
    return sys.argv[0]


def getDest():
    return os.environ.get(NLDEST_ENV, None)


class LevelConfig:
    """Set logging level from a configuration file.
    The format of the file is trivial: an integer log level.
    """
    DEFAULT = Level.INFO

    def __init__(self, filename):
        self._f = filename
        self._level = None
        return

    def getLevel(self):
        if self._level is None:
            try:
                self._level = self.DEFAULT
                f = file(self._f)
                line = f.readline()
                i = int(line.strip())
                self._level = i
            except IOError:
                pass
            except ValueError:
                pass

        return self._level


if os.getenv(CFG_ENV) != None:
    g_level_cfg = LevelConfig(os.getenv(CFG_ENV))
else:
    g_level_cfg = None

class Log:
    """NetLogger log class.
    
    Name=value pairs for the log are passed as keyword arguments.
    This is mostly good, but one drawback is that a period '.' in the
    name is confusing to python. As a work-around, use '__' to mean '.', 
    e.g. if you want the result to be "foo.id=bar", then do::
        log.write(.., foo__id='bar')
    Similarly, a leading '__' will be stripped (e.g. to avoid stepping
    on keywords like 'class')
    
    If you instantiate this class without a 'logfile', it will act
    as a formatter, returning a string.

    To disable filtering of messages on level, add 'level=Level.ALL'
    """

    class OpenError(Exception):
        pass

    def __init__(self, logfile=None, flush=False, prefix=None, level=Level.INFO, newline=True, guid=True, pretty=False, float_time=False, meta={}):
        """Constructor.
        """
        self._logfile = None
        self._float_time = float_time
        self._pretty = pretty
        self._newline = newline
        self._flush = [None, self.flush][flush]
        self.setPrefix(prefix)
        self._meta = {}
        if meta:
            self._meta[None] = meta
        if isinstance(logfile, types.StringType):
            try:
                self._logfile = urlfile(logfile)
            except (socket.gaierror, socket.error, IOError), E:
                raise self.OpenError(E)

        else:
            self._logfile = logfile
        if g_level_cfg is None:
            self._level = level
        else:
            self._level = g_level_cfg.getLevel()
        if guid is True:
            guid = getGuid(create=False)
            if guid:
                _m = self._meta.get(None, {})
                _m['guid'] = guid
                self._meta[None] = _m
        elif isinstance(guid, str):
            _m = self._meta.get(None, {})
            _m['guid'] = guid
            self._meta[None] = _m
        return

    def setLevel(self, level):
        """Set highest level of messages that WILL be logged.
        Messages below this level (that is, less severe,
        higher numbers) will be dropped.

        For example::
          log.setLevel(Level.WARN)
          log.error('argh',{}) # logged
          log.info('whatever',{}) # dropped!
        """
        self._level = level

    def setPrefix(self, prefix):
        if prefix is None:
            self._pfx = ''
        elif prefix.endswith('.'):
            self._pfx = prefix
        else:
            self._pfx = prefix + '.'
        return

    def debugging(self):
        """Return whether the level >= debug.
        """
        return self._level >= Level.DEBUG

    def flush(self):
        """Flush output object.
        """
        if self._logfile:
            self._logfile.flush()

    def write(self, event='event', ts=None, level=Level.INFO, **kw):
        """Write a NetLogger string.
           If there is a logfile, returns None
           Otherwise, returns a string that would have been written.
        """
        if self._level != Level.ALL and level > self._level:
            if self._logfile:
                return
            else:
                return ''
        if not ts:
            ts = time.time()
        buf = self.format(self._pfx + event, ts, level, kw)
        if self._logfile is None:
            return buf
        else:
            self._logfile.write(buf)
            if self._flush:
                self.flush()
            return

    __call__ = write

    def error(self, event='', **kwargs):
        return self.write(event, level=Level.ERROR, **kwargs)

    def warn(self, event='', **kwargs):
        return self.write(event, level=Level.WARN, **kwargs)

    def info(self, event='', **kwargs):
        return self.write(event, level=Level.INFO, **kwargs)

    def debug(self, event='', **kwargs):
        return self.write(event, level=Level.DEBUG, **kwargs)

    def _append(self, fields, kw):
        for (k, v) in kw.items():
            if k.startswith('__'):
                k = k[2:]
            k = k.replace('__', '.')
            if isinstance(v, str):
                v = quotestr(v)
                fields.append('%s=%s' % (k, v))
            elif isinstance(v, float):
                fields.append('%s=%lf' % (k, v))
            elif isinstance(v, int):
                fields.append('%s=%d' % (k, v))
            else:
                s = str(v)
                if ' ' in s or '\t' in s:
                    s = '"%s"' % s
                fields.append('%s=%s' % (k, s))

    def format(self, event, ts, level, kw):
        if not self._pretty:
            if isinstance(ts, str):
                fields = [
                 'ts=' + ts, 'event=' + event]
            elif isinstance(ts, datetime.datetime):
                if self._float_time:
                    tsfloat = calendar.timegm(ts.utctimetuple()) + ts.microsecond / 1000000.0
                    fields = ['ts=%.6f' % tsfloat, 'event=' + event]
                else:
                    tsstr = '%s.%06dZ' % (DATE_FMT % ts.utctimetuple()[0:6],
                     ts.microsecond)
                    fields = ['ts=' + tsstr, 'event=' + event]
            elif self._float_time:
                fields = [
                 'ts=%.6f' % ts, 'event=' + event]
            else:
                fields = [
                 'ts=' + utcFormatISO(ts), 'event=' + event]
            if level is not None:
                if isinstance(level, int):
                    fields.append('level=' + Level.getName(level))
                else:
                    fields.append('level=%s' % level)
            if kw:
                self._append(fields, kw)
            if self._meta.has_key(event):
                self._append(fields, self._meta[event])
            if self._meta.has_key(None):
                self._append(fields, self._meta[None])
            buf = FIELD_SEP.join(fields)
        else:
            if not isinstance(ts, str):
                ts = utcFormatISO(ts)
            if isinstance(level, int):
                level = Level.getName(level).upper()
            if kw.has_key('traceback'):
                tbstr = kw['traceback']
                del kw['traceback']
            else:
                tbstr = None
            if kw.has_key('msg'):
                msg = kw['msg']
                del kw['msg']
            else:
                msg = None
            remainder = (',').join([ '%s=%s' % (key, value) for (key, value) in kw.items()
                                   ])
            if msg:
                buf = '%s %-6s %s | %s. %s' % (ts, level, event, msg, remainder)
            else:
                buf = '%s %-6s %s | %s' % (ts, level, event, remainder)
            if tbstr:
                buf += '\n' + tbstr
        if self._newline:
            return buf + REC_SEP
        else:
            return buf
            return

    def setMeta(self, event=None, **kw):
        self._meta[event] = kw

    def close(self):
        self.flush()

    def __del__(self):
        if not hasattr(self, 'closed'):
            self.close()
        self.closed = True

    def __str__(self):
        if self._logfile:
            return str(self._logfile)
        else:
            return repr(self)


for scheme in ('x-netlog', 'x-netlog-udp'):
    urlparse.uses_netloc.append(scheme)
    urlparse.uses_query.append(scheme)

def urlfile(url):
    """urlfile(url:str) -> file

    Open a NetLogger URL and return a write-only file object.
    """
    (scheme, netloc, path, params, query, frag) = urlparse.urlparse(url)
    query_data = {}
    if query:
        query_parts = query.split('&')
        for flag in query_parts:
            (name, value) = flag.split('=')
            query_data[name] = value

    if scheme == 'file' or scheme == '' or scheme is None:
        if path == '-':
            fileobj = sys.stdout
        elif path == '&':
            fileobj = sys.stderr
        else:
            if query_data.has_key('append'):
                is_append = boolparse(query_data['append'])
                open_flag = 'aw'[is_append]
            else:
                open_flag = 'a'
            fileobj = file(path, open_flag)
    elif scheme.startswith('x-netlog'):
        if netloc.find(':') == -1:
            addr = (
             netloc, DEFAULT_PORT)
        else:
            (host, port_str) = netloc.split(':')
            addr = (host, int(port_str))
        if scheme == 'x-netlog':
            sock = socket.socket()
        elif scheme == 'x-netlog-udp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            raise ValueError("Unknown URL scheme '%s', must be empty, 'file' or 'x-netlog[-udp]'" % scheme)
        sock.connect(addr)
        fileobj = sock.makefile('w')
    else:
        raise ValueError("Unknown URL scheme '%s', must be empty, 'file' or 'x-netlog[-udp]'" % scheme)
    return fileobj


def urltype(url):
    """urltype(url:str) -> 'file' | 'tcp' | None

    Return a canonical string representing the type of URL,
    or None if the type is unknown
    """
    scheme = urlparse.urlparse(url)[0]
    if scheme == 'file' or scheme == '' or scheme is None:
        return 'file'
    else:
        if scheme == 'x-netlog':
            return 'tcp'
        else:
            return
        return


_g_hostip = None

def get_host():
    global _g_hostip
    if _g_hostip is not None:
        return _g_hostip
    else:
        try:
            ip = socket.gethostbyname(socket.getfqdn())
        except:
            ip = '127.0.0.1'

        _g_hostip = ip
        return ip