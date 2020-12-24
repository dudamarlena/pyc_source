# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/utils.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 14872 bytes
"""Useful utility functions."""
import signal, datetime, hashlib, locale, logging, os, pkgutil, stat, time, urllib.request, urllib.parse, urllib.error, string, threading
from functools import reduce
from collections import namedtuple
import yaml, jinja2, treadmill
from . import subproc
if os.name != 'nt':
    import fcntl
threading._DummyThread._Thread__stop = lambda x: 0
_LOGGER = logging.getLogger(__name__)
JINJA2_ENV = jinja2.Environment(loader=jinja2.PackageLoader(__name__))
EXEC_MODE = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IWUSR | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
_DEFAULT_BASE_ALPHABET = string.digits + string.ascii_lowercase

def create_script(path, templatename, mode=EXEC_MODE, *args, **kwargs):
    """This Creates a file from a JINJA template.

    The templates exist in our lib/python/templates directory.

    templatename - The name of the template file.
    mode - The mode for the file.  Defaults to +x
    args and kwargs are passed into the template."""
    template = JINJA2_ENV.get_template(templatename)
    all_kwargs = {}
    if subproc.EXECUTABLES:
        all_kwargs.update(subproc.EXECUTABLES)
    all_kwargs.update(kwargs)
    with open(path, 'w') as (f):
        f.write(template.render(*args, **all_kwargs))
    os.chmod(path, int(mode))


def ip2int(ip_addr):
    """Converts string IP address representation into integer."""
    i = [int(x) for x in ip_addr.split('.')]
    return i[0] << 24 | i[1] << 16 | i[2] << 8 | i[3]


def int2ip(ip_addr_int32):
    """Converts integer to IP address string."""

    def _int2ip(ip_addr_int32, offset, acc):
        """Shift / recursive conversion of int32 to IP parts."""
        if offset == 0:
            acc.append(str(ip_addr_int32))
        else:
            acc.append(str(ip_addr_int32 >> offset))
            _int2ip(ip_addr_int32 - (ip_addr_int32 >> offset << offset), offset - 8, acc)

    acc = []
    _int2ip(ip_addr_int32, 24, acc)
    return '.'.join(acc)


def to_obj(value, name='struct'):
    """Recursively converts dictionary and lists to namedtuples."""
    if isinstance(value, list):
        return [to_obj(item) for item in value]
    else:
        if isinstance(value, dict):
            return namedtuple(name, value.keys())(*[to_obj(v, k) for k, v in value.items()])
        return value


def sys_exit(code):
    """Exit using os._exit, bypassing any on_exit code.

    Should be used in a child process after fork().
    """
    _LOGGER.debug('os._exit, rc: %d', code)
    os._exit(code)


def _repr_unicode(dumper, data):
    """Fix yaml str representation."""
    data = data.encode('ascii', 'ignore').decode()
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    else:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def _repr_tuple(dumper, data):
    """Fix yaml tuple representation (use list)."""
    return dumper.represent_list(list(data))


def _repr_none(dumper, data_unused):
    """Fix yaml None representation (use ~)."""
    return dumper.represent_scalar('tag:yaml.org,2002:null', '~')


yaml.add_representer(str, _repr_unicode)
yaml.add_representer(tuple, _repr_tuple)
yaml.add_representer(type(None), _repr_none)

def dump_yaml(obj):
    """Returns yaml representation of the object."""
    return yaml.dump(obj, default_flow_style=False, explicit_start=True, explicit_end=True)


def print_yaml(obj):
    """Print yaml wih correct options."""
    print(dump_yaml(obj))


def hashcmp(file1, file2):
    """Compare two files based on sha1 hash value."""
    sha1 = hashlib.sha1()
    sha2 = hashlib.sha1()
    with open(file1, 'rb') as (f):
        data = f.read()
        sha1.update(data)
    with open(file2, 'rb') as (f):
        data = f.read()
        sha2.update(data)
    return sha1.hexdigest() == sha2.hexdigest()


def rootdir():
    """Returns install root of the Treadmill framework."""
    if 'TREADMILL' in os.environ:
        return os.environ['TREADMILL']
    raise Exception('Must have TREADMILL env variable.')


def distro():
    """Returns root of the codebase."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), '../../..'))


def touch(filename):
    """'Touch' a filename."""
    with open(filename, 'a') as (f):
        os.fchown(f.fileno(), -1, -1)


class FileLock(object):
    __doc__ = 'Utility file based lock.'

    def __init__(self, filename):
        self.fd = open(filename + '.lock', 'w')

    def __enter__(self):
        fcntl.flock(self.fd, fcntl.LOCK_EX)

    def __exit__(self, type_unused, value_unused, traceback_unused):
        fcntl.flock(self.fd, fcntl.LOCK_UN)
        self.fd.close()


def cpu_units(value):
    """Converts CPU string into numeric in BMIPS"""
    norm = str(value).upper().strip()
    if norm.endswith('%'):
        return int(norm[:-1])
    else:
        return int(norm)


_SIZE_SCALE = {x[1]:x[0] for x in enumerate(['B', 'K', 'M', 'G', 'T',
 'P', 'E', 'Z', 'Y'])}

def size_to_bytes(size):
    """Convert a human friendly size string into a size in bytes.

    Properly handles input values with suffix (M, G, T, P, E, Z, Y) and an
    optional 'B' suffix modifier (MB, GB, TB, PB, EB, ZB, YB).

    If size is an integer, it is assumed to be in bytes already.

    :param size:
        `size` optionally followed by a suffix.
    :type size:
        ``str`` | ``int``
    :returns:
        (``int``) -- `size` in bytes

    *Examples*:

    .. testsetup::

        from treadmill.utils import size_to_bytes

    >>> size_to_bytes("1KB")
    1000
    >>> size_to_bytes("1K")
    1024
    """
    if isinstance(size, str):
        size = str(size).upper().strip()
        unit = 1024
        if size[(-1)] == 'B':
            unit = 1000
            size = size[:-1]
        if size[(-1)] in _SIZE_SCALE:
            return int(size[:-1]) * pow(unit, _SIZE_SCALE[size[(-1)]])
        else:
            return int(size)
    else:
        return int(size)


def kilobytes(value):
    """Converts values with M/K/G suffix into numeric in Kbytes.

    The following are valid strings:
    10K
    10M
    10G
    10 (default kb)
    """
    norm = str(value).upper().strip()
    if norm == '0':
        return 0
    if norm[(-1)] not in _SIZE_SCALE:
        _LOGGER.error('Invalid (unitless) value: %s', value)
        raise Exception('Invalid (unitless) value: ' + str(value))
    return size_to_bytes(value) / 1024


def megabytes(value):
    """Converts values with M/K/G suffix info numeric in Mbytes"""
    return kilobytes(value) / 1024


def validate(struct, schema):
    """Validate dictionary required fields.

    The schema is a list of tuples (field, required, field_type). For each
    tuple the function will check that required field is present and that it is
    of expected type. If not required field is missing, it will be initialize
    with the type constructor.
    """
    if not isinstance(struct, dict):
        raise treadmill.exc.InvalidInputError(struct, 'Expected dict.')
    for field, required, ftype in schema:
        if field not in struct:
            if required:
                raise treadmill.exc.InvalidInputError(struct, 'Required field: %s' % field)
            else:
                struct[field] = ftype()
        if not isinstance(struct[field], ftype):
            raise treadmill.exc.InvalidInputError(struct, 'Invalid type for %s, expected: %s' % (
             field, str(ftype)))
            continue


_TIME_SCALE = {'S': 1,  'M': 60,  'H': 3600, 
 'D': 86400}

def to_seconds(value):
    """Converts values with s/m/d suffix into numeric in seconds."""
    norm = str(value).upper().strip()
    if norm[(-1)] not in _TIME_SCALE:
        _LOGGER.error('Invalid (unitless) interval: %s', value)
        raise Exception('Invalid (unitless) interval: ' + str(value))
    return int(norm[0:-1]) * _TIME_SCALE[norm[(-1)]]


def bytes_to_readable(num, power='M'):
    """Converts numerical value into human readable memory value."""
    powers = [
     'B', 'K', 'M', 'G', 'T']
    while num >= 1000:
        num /= 1024.0
        next_power_idx = powers.index(power) + 1
        if next_power_idx == len(powers):
            break
        power = powers[next_power_idx]

    return '%.1f%s' % (num, power)


def cpu_to_readable(num):
    """Converts CPU % into readable number."""
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    return locale.format('%d', num, grouping=True)


def cpu_to_cores_readable(num):
    """Converts CPU % into number of abstract cores."""
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    return locale.format('%.2f', num / 100.0, grouping=True)


def ratio_to_readable(value):
    """Converts ratio to human readable percentage."""
    return '%.1f' % (value / 100.0)


def find_in_path(prog):
    """Search for application in system path and returns the full path."""
    if os.path.isabs(prog):
        return prog
    for path in os.environ.get('PATH', '').split(':'):
        fullpath = os.path.join(path, prog)
        if os.path.exists(fullpath) and os.access(fullpath, os.X_OK):
            return fullpath

    return prog


def tail_stream(stream, nlines=10):
    """Returns last N lines from the io object (file or io.string)."""
    stream.seek(0, 2)
    fsize = stream.tell()
    stream.seek(max(fsize - 1024, 0), 0)
    lines = stream.readlines()
    return lines[-nlines:]


def tail(filename, nlines=10):
    """Retuns last N lines from the file."""
    try:
        with open(filename) as (f):
            return tail_stream(f, nlines=nlines)
    except Exception:
        _LOGGER.error('Cannot open %s for reading.', filename)
        return []


def datetime_utcnow():
    """Wrapper for datetime.datetime.utcnow for testability."""
    return datetime.datetime.utcnow()


def strftime_utc(epoch):
    """Convert seconds from epoch into UTC time string."""
    return time.strftime('%a, %d %b %Y %H:%M:%S+0000', time.gmtime(epoch))


def to_base_n(num, base=None, alphabet=None):
    """Encode a number in base X using a given alphabet

    :param int number:
        Number to encode
    :param int base:
        Length of the base to use
    :param str alphabet:
        The alphabet to use for encoding
    """
    if alphabet is None:
        alphabet = _DEFAULT_BASE_ALPHABET
    if base is None:
        base = len(alphabet)
    if not 0 <= base <= len(alphabet):
        raise ValueError('Invalid base length: %s' % base)
    if num == 0:
        return alphabet[0]
    arr = []
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])

    arr.reverse()
    return ''.join(arr)


def from_base_n(base_num, base=None, alphabet=None):
    """Decode a Base X encoded string into the number

    :param str base_num:
        Number encoded in the given base
    :param int base:
        Length of the base to use
    :param str alphabet:
        The alphabet to use for encoding
    """
    if alphabet is None:
        alphabet = _DEFAULT_BASE_ALPHABET
    if base is None:
        base = len(alphabet)
    if not 0 <= base <= len(alphabet):
        raise ValueError('Invalid base length: %s' % base)
    strlen = len(base_num)
    num = 0
    idx = 0
    for char in base_num:
        power = strlen - (idx + 1)
        num += alphabet.index(char) * base ** power
        idx += 1

    return num


def report_ready():
    """Reports the service as ready for s6-svwait -U."""
    try:
        with open('notification-fd') as (f):
            try:
                fd = int(f.readline())
                os.write(fd, 'ready\n')
                os.close(fd)
            except OSError:
                _LOGGER.exception('Cannot read notification-fd')

    except IOError:
        _LOGGER.warn('notification-fd does not exist.')


def drop_privileges(uid_name='nobody'):
    """Drop root privileges."""
    if os.getuid() != 0:
        return
    import pwd
    running_uid = pwd.getpwnam(uid_name).pw_uid
    os.setgroups([])
    os.setuid(running_uid)
    os.umask(63)
    os.environ['KRB5CCNAME'] = 'FILE:/no_such_krbcc'


_SIG2NAME = {getattr(signal, attr):attr for attr in dir(signal) if attr.startswith('SIG') and '_' not in attr if attr.startswith('SIG') and '_' not in attr}

def signal2name(num):
    """Convert signal number to signal name."""
    return _SIG2NAME.get(num, num)


def make_signal_flag(*signals):
    """Return a flag that will be set when process is signaled."""
    _LOGGER.info('Configuring signal flag: %r', signals)
    signalled = set()

    def _handler(signum, frame_unused):
        """Signal handler."""
        signalled.add(signum)

    for signum in signals:
        signal.signal(signum, _handler)

    return signalled


def compose(*funcs):
    """Compose functions."""
    return lambda x: reduce(lambda v, f: f(v), reversed(funcs), x)


def modules_in_pkg(pkg):
    """Get the modules in the provided package

    :param pkg: the full package
    :type pkg: module
    """
    modules = []
    for _importer, modname, ispkg in pkgutil.walk_packages(pkg.__path__):
        if ispkg:
            continue
        modules.append(modname)

    return modules


def equals_list2dict(equals_list):
    """Converts an array of key/values seperated by = to dict"""
    return dict(entry.split('=') for entry in equals_list)


def encode_uri_parts(path):
    """Encode URI path components"""
    return '/'.join([urllib.parse.quote(part) for part in path.split('/')])