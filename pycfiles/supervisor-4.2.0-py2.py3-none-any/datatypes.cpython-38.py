# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/datatypes.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 13245 bytes
import grp, os, pwd, signal, socket, shlex
from supervisor.compat import urlparse
from supervisor.compat import long
from supervisor.loggers import getLevelNumByDescription

def process_or_group_name(name):
    """Ensures that a process or group name is not created with
       characters that break the eventlistener protocol or web UI URLs"""
    s = str(name).strip()
    for character in ' :/':
        if character in s:
            raise ValueError('Invalid name: %r because of character: %r' % (name, character))
        return s


def integer--- This code section failed: ---

 L.  22         0  SETUP_FINALLY        12  'to 12'

 L.  23         2  LOAD_GLOBAL              int
                4  LOAD_FAST                'value'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  24        12  DUP_TOP          
               14  LOAD_GLOBAL              ValueError
               16  LOAD_GLOBAL              OverflowError
               18  BUILD_TUPLE_2         2 
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    42  'to 42'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  25        30  LOAD_GLOBAL              long
               32  LOAD_FAST                'value'
               34  CALL_FUNCTION_1       1  ''
               36  ROT_FOUR         
               38  POP_EXCEPT       
               40  RETURN_VALUE     
             42_0  COME_FROM            22  '22'
               42  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 26


TRUTHY_STRINGS = ('yes', 'true', 'on', '1')
FALSY_STRINGS = ('no', 'false', 'off', '0')

def boolean(s):
    """Convert a string value to a boolean value."""
    ss = str(s).lower()
    if ss in TRUTHY_STRINGS:
        return True
    if ss in FALSY_STRINGS:
        return False
    raise ValueError('not a valid boolean value: ' + repr(s))


def list_of_strings--- This code section failed: ---

 L.  41         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L.  42         4  BUILD_LIST_0          0 
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L.  43         8  SETUP_FINALLY        32  'to 32'

 L.  44        10  LOAD_LISTCOMP            '<code_object <listcomp>>'
               12  LOAD_STR                 'list_of_strings.<locals>.<listcomp>'
               14  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               16  LOAD_FAST                'arg'
               18  LOAD_METHOD              split
               20  LOAD_STR                 ','
               22  CALL_METHOD_1         1  ''
               24  GET_ITER         
               26  CALL_FUNCTION_1       1  ''
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY     8  '8'

 L.  45        32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  46        38  LOAD_GLOBAL              ValueError
               40  LOAD_STR                 'not a valid list of strings: '
               42  LOAD_GLOBAL              repr
               44  LOAD_FAST                'arg'
               46  CALL_FUNCTION_1       1  ''
               48  BINARY_ADD       
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
               54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 52


def list_of_ints--- This code section failed: ---

 L.  49         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L.  50         4  BUILD_LIST_0          0 
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L.  52         8  SETUP_FINALLY        32  'to 32'

 L.  53        10  LOAD_GLOBAL              list
               12  LOAD_GLOBAL              map
               14  LOAD_GLOBAL              int
               16  LOAD_FAST                'arg'
               18  LOAD_METHOD              split
               20  LOAD_STR                 ','
               22  CALL_METHOD_1         1  ''
               24  CALL_FUNCTION_2       2  ''
               26  CALL_FUNCTION_1       1  ''
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY     8  '8'

 L.  54        32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  55        38  LOAD_GLOBAL              ValueError
               40  LOAD_STR                 'not a valid list of ints: '
               42  LOAD_GLOBAL              repr
               44  LOAD_FAST                'arg'
               46  CALL_FUNCTION_1       1  ''
               48  BINARY_ADD       
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
               54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 52


def list_of_exitcodes--- This code section failed: ---

 L.  58         0  SETUP_FINALLY        54  'to 54'

 L.  59         2  LOAD_GLOBAL              list_of_ints
                4  LOAD_FAST                'arg'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'vals'

 L.  60        10  LOAD_FAST                'vals'
               12  GET_ITER         
             14_0  COME_FROM            32  '32'
               14  FOR_ITER             48  'to 48'
               16  STORE_FAST               'val'

 L.  61        18  LOAD_FAST                'val'
               20  LOAD_CONST               255
               22  COMPARE_OP               >
               24  POP_JUMP_IF_TRUE     34  'to 34'
               26  LOAD_FAST                'val'
               28  LOAD_CONST               0
               30  COMPARE_OP               <
               32  POP_JUMP_IF_FALSE    14  'to 14'
             34_0  COME_FROM            24  '24'

 L.  62        34  LOAD_GLOBAL              ValueError
               36  LOAD_STR                 'Invalid exit code "%s"'
               38  LOAD_FAST                'val'
               40  BINARY_MODULO    
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  JUMP_BACK            14  'to 14'

 L.  63        48  LOAD_FAST                'vals'
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY     0  '0'

 L.  64        54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L.  65        60  LOAD_GLOBAL              ValueError
               62  LOAD_STR                 'not a valid list of exit codes: '
               64  LOAD_GLOBAL              repr
               66  LOAD_FAST                'arg'
               68  CALL_FUNCTION_1       1  ''
               70  BINARY_ADD       
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
               80  END_FINALLY      
             82_0  COME_FROM            78  '78'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 74


def dict_of_key_value_pairs(arg):
    """ parse KEY=val,KEY2=val2 into {'KEY':'val', 'KEY2':'val2'}
        Quotes can be used to allow commas in the value
    """
    lexer = shlex.shlexstr(arg)
    lexer.wordchars += '/.+-():'
    tokens = list(lexer)
    tokens_len = len(tokens)
    D = {}
    i = 0
    while i < tokens_len:
        k_eq_v = tokens[i:i + 3]
        if not len(k_eq_v) != 3:
            if k_eq_v[1] != '=':
                raise ValueError("Unexpected end of key/value pairs in value '%s'" % arg)
            D[k_eq_v[0]] = k_eq_v[2].strip'\'"'
            i += 4

    return D


class Automatic:
    pass


LOGFILE_NONES = ('none', 'off', None)
LOGFILE_AUTOS = (Automatic, 'auto')

def logfile_name(val):
    if hasattr(val, 'lower'):
        coerced = val.lower()
    else:
        coerced = val
    if coerced in LOGFILE_NONES:
        return
    if coerced in LOGFILE_AUTOS:
        return Automatic
    return existing_dirpath(val)


class RangeCheckedConversion:
    __doc__ = 'Conversion helper that range checks another conversion.'

    def __init__(self, conversion, min=None, max=None):
        self._min = min
        self._max = max
        self._conversion = conversion

    def __call__(self, value):
        v = self._conversionvalue
        if self._min is not None:
            if v < self._min:
                raise ValueError('%s is below lower bound (%s)' % (
                 repr(v), repr(self._min)))
        if self._max is not None:
            if v > self._max:
                raise ValueError('%s is above upper bound (%s)' % (
                 repr(v), repr(self._max)))
        return v


port_number = RangeCheckedConversion(integer, min=1, max=65535).__call__

def inet_address(s):
    host = ''
    if ':' in s:
        host, s = s.split(':', 1)
        if not s:
            raise ValueError('no port number specified in %r' % s)
        port = port_number(s)
        host = host.lower()
    else:
        try:
            port = port_number(s)
        except ValueError:
            raise ValueError('not a valid port number: %r ' % s)
        else:
            if not host or host == '*':
                host = ''
            return (
             host, port)


class SocketAddress:

    def __init__(self, s):
        if not '/' in s:
            if s.findos.sep >= 0 or ':' not in s:
                self.family = getattr(socket, 'AF_UNIX', None)
                self.address = s
        else:
            self.family = socket.AF_INET
            self.address = inet_address(s)


class SocketConfig:
    __doc__ = ' Abstract base class which provides a uniform abstraction\n    for TCP vs Unix sockets '
    url = ''
    addr = None
    backlog = None

    def __repr__(self):
        return '<%s at %s for %s>' % (self.__class__,
         id(self),
         self.url)

    def __str__(self):
        return str(self.url)

    def __eq__(self, other):
        if not isinstance(other, SocketConfig):
            return False
        if self.url != other.url:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__other

    def get_backlog(self):
        return self.backlog

    def addr(self):
        raise NotImplementedError

    def create_and_bind(self):
        raise NotImplementedError


class InetStreamSocketConfig(SocketConfig):
    __doc__ = ' TCP socket config helper '
    host = None
    port = None

    def __init__(self, host, port, **kwargs):
        self.host = host.lower()
        self.port = port_number(port)
        self.url = 'tcp://%s:%d' % (self.host, self.port)
        self.backlog = kwargs.get('backlog', None)

    def addr(self):
        return (
         self.host, self.port)

    def create_and_bind(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bindself.addr()
        except:
            sock.close()
            raise
        else:
            return sock


class UnixStreamSocketConfig(SocketConfig):
    __doc__ = ' Unix domain socket config helper '
    path = None
    mode = None
    owner = None
    sock = None

    def __init__(self, path, **kwargs):
        self.path = path
        self.url = 'unix://%s' % path
        self.mode = kwargs.get('mode', None)
        self.owner = kwargs.get('owner', None)
        self.backlog = kwargs.get('backlog', None)

    def addr(self):
        return self.path

    def create_and_bind(self):
        if os.path.existsself.path:
            os.unlinkself.path
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.bindself.addr()
            self._chown()
            self._chmod()
        except:
            sock.close()
            if os.path.existsself.path:
                os.unlinkself.path
            raise
        else:
            return sock

    def get_mode(self):
        return self.mode

    def get_owner(self):
        return self.owner

    def _chmod(self):
        if self.mode is not None:
            try:
                os.chmod(self.path, self.mode)
            except Exception as e:
                try:
                    raise ValueError('Could not change permissions of socket ' + 'file: %s' % e)
                finally:
                    e = None
                    del e

    def _chown(self):
        if self.owner is not None:
            try:
                os.chown(self.path, self.owner[0], self.owner[1])
            except Exception as e:
                try:
                    raise ValueError('Could not change ownership of socket file: ' + '%s' % e)
                finally:
                    e = None
                    del e


def colon_separated_user_group--- This code section failed: ---

 L. 276         0  SETUP_FINALLY        78  'to 78'

 L. 277         2  LOAD_FAST                'arg'
                4  LOAD_METHOD              split
                6  LOAD_STR                 ':'
                8  LOAD_CONST               1
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'parts'

 L. 278        14  LOAD_GLOBAL              len
               16  LOAD_FAST                'parts'
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_CONST               1
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    44  'to 44'

 L. 279        26  LOAD_GLOBAL              name_to_uid
               28  LOAD_FAST                'parts'
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'uid'

 L. 280        38  LOAD_CONST               -1
               40  STORE_FAST               'gid'
               42  JUMP_FORWARD         68  'to 68'
             44_0  COME_FROM            24  '24'

 L. 282        44  LOAD_GLOBAL              name_to_uid
               46  LOAD_FAST                'parts'
               48  LOAD_CONST               0
               50  BINARY_SUBSCR    
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'uid'

 L. 283        56  LOAD_GLOBAL              name_to_gid
               58  LOAD_FAST                'parts'
               60  LOAD_CONST               1
               62  BINARY_SUBSCR    
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'gid'
             68_0  COME_FROM            42  '42'

 L. 284        68  LOAD_FAST                'uid'
               70  LOAD_FAST                'gid'
               72  BUILD_TUPLE_2         2 
               74  POP_BLOCK        
               76  RETURN_VALUE     
             78_0  COME_FROM_FINALLY     0  '0'

 L. 285        78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 286        84  LOAD_GLOBAL              ValueError
               86  LOAD_STR                 'Invalid user:group definition %s'
               88  LOAD_FAST                'arg'
               90  BINARY_MODULO    
               92  CALL_FUNCTION_1       1  ''
               94  RAISE_VARARGS_1       1  'exception instance'
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 94


def name_to_uid(name):
    """ Find a user ID from a string containing a user name or ID.
        Raises ValueError if the string can't be resolved to a valid
        user ID on the system. """
    try:
        uid = int(name)
    except ValueError:
        try:
            pwdrec = pwd.getpwnamname
        except KeyError:
            raise ValueError('Invalid user name %s' % name)
        else:
            uid = pwdrec[2]
    else:
        try:
            pwd.getpwuiduid
        except KeyError:
            raise ValueError('Invalid user id %s' % name)
        else:
            return uid


def name_to_gid(name):
    """ Find a group ID from a string containing a group name or ID.
        Raises ValueError if the string can't be resolved to a valid
        group ID on the system. """
    try:
        gid = int(name)
    except ValueError:
        try:
            grprec = grp.getgrnamname
        except KeyError:
            raise ValueError('Invalid group name %s' % name)
        else:
            gid = grprec[2]
    else:
        try:
            grp.getgrgidgid
        except KeyError:
            raise ValueError('Invalid group id %s' % name)
        else:
            return gid


def gid_for_uid(uid):
    pwrec = pwd.getpwuiduid
    return pwrec[3]


def octal_type--- This code section failed: ---

 L. 331         0  SETUP_FINALLY        14  'to 14'

 L. 332         2  LOAD_GLOBAL              int
                4  LOAD_FAST                'arg'
                6  LOAD_CONST               8
                8  CALL_FUNCTION_2       2  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 333        14  DUP_TOP          
               16  LOAD_GLOBAL              TypeError
               18  LOAD_GLOBAL              ValueError
               20  BUILD_TUPLE_2         2 
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    48  'to 48'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 334        32  LOAD_GLOBAL              ValueError
               34  LOAD_STR                 '%s can not be converted to an octal type'
               36  LOAD_FAST                'arg'
               38  BINARY_MODULO    
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            24  '24'
               48  END_FINALLY      
             50_0  COME_FROM            46  '46'

Parse error at or near `POP_TOP' instruction at offset 28


def existing_directory(v):
    nv = os.path.expanduserv
    if os.path.isdirnv:
        return nv
    raise ValueError('%s is not an existing directory' % v)


def existing_dirpath(v):
    nv = os.path.expanduserv
    dir = os.path.dirnamenv
    if not dir:
        return nv
    if os.path.isdirdir:
        return nv
    raise ValueError('The directory named as part of the path %s does not exist' % v)


def logging_level(value):
    s = str(value).lower()
    level = getLevelNumByDescription(s)
    if level is None:
        raise ValueError('bad logging level name %r' % value)
    return level


class SuffixMultiplier:

    def __init__(self, d, default=1):
        self._d = d
        self._default = default
        self._keysz = None
        for k in d.keys():
            if self._keysz is None:
                self._keysz = len(k)
            elif not self._keysz == len(k):
                raise AssertionError

    def __call__(self, v):
        v = v.lower()
        for s, m in self._d.items():
            if v[-self._keysz:] == s:
                return int(v[:-self._keysz]) * m
            return int(v) * self._default


byte_size = SuffixMultiplier({'kb':1024,  'mb':1048576, 
 'gb':1048576 * long(1024)})

def url(value):
    uri = value.replace('unix://', 'http://', 1).strip()
    scheme, netloc, path, params, query, fragment = urlparse.urlparseuri
    if scheme:
        if netloc or path:
            return value
    raise ValueError('value %r is not a URL' % value)


SIGNUMS = [getattr(signal, k) for k in dir(signal) if k.startswith'SIG']

def signal_number(value):
    try:
        num = int(value)
    except (ValueError, TypeError):
        name = value.strip().upper()
        if not name.startswith'SIG':
            name = 'SIG' + name
        num = getattr(signal, name, None)
        if num is None:
            raise ValueError('value %r is not a valid signal name' % value)
    else:
        if num not in SIGNUMS:
            raise ValueError('value %r is not a valid signal number' % value)
        return num


class RestartWhenExitUnexpected:
    pass


class RestartUnconditionally:
    pass


def auto_restart(value):
    value = str(value.lower())
    computed_value = value
    if value in TRUTHY_STRINGS:
        computed_value = RestartUnconditionally
    else:
        if value in FALSY_STRINGS:
            computed_value = False
        else:
            if value == 'unexpected':
                computed_value = RestartWhenExitUnexpected
    if computed_value not in (RestartWhenExitUnexpected,
     RestartUnconditionally, False):
        raise ValueError("invalid 'autorestart' value %r" % value)
    return computed_value


def profile_options(value):
    options = [x.lower() for x in list_of_strings(value)]
    sort_options = []
    callers = False
    for thing in options:
        if thing != 'callers':
            sort_options.appendthing
        else:
            callers = True
    else:
        return (
         sort_options, callers)