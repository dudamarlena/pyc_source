# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/flask-magic/flask_magic/utils.py
# Compiled at: 2016-07-19 00:12:49
# Size of source mod 2**32: 9309 bytes
"""
Some common functions
"""
from __future__ import division
import inspect, os, re, string, random, socket, subprocess, functools, multiprocessing, threading
from passlib.hash import bcrypt as crypt_engine
from six.moves.urllib.parse import urlparse
import datetime, humanize, pkg_resources, urllib, hashlib, json
from slugify import slugify
from inflection import dasherize, underscore, camelize, pluralize, singularize, titleize
from werkzeug.utils import import_string

def is_email_valid(email):
    """
    Check if email is valid
    """
    pattern = re.compile('[\\w\\.-]+@[\\w\\.-]+[.]\\w+')
    return bool(pattern.match(email))


def is_password_valid(password):
    """
    Check if a password is valid
    """
    pattern = re.compile('^.{4,75}$')
    return bool(pattern.match(password))


def is_url_valid(url):
    """
    Check if url is valid
    """
    pattern = re.compile('^(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+(?:[A-Z]{2,6}\\.?|[A-Z0-9-]{2,}\\.?)|\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})(?::\\d+)?(?:/?|[/?]\\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))


def urlencode(s):
    return urllib.quote(s)


def urldecode(s):
    return urllib.unquote(s).decode('utf8')


def md5(value):
    """
    Create MD5
    :param value:
    :return:
    """
    if isinstance(value, (list, dict)):
        value = json.dumps(value)
    m = hashlib.md5()
    m.update(value)
    return str(m.hexdigest())


def chunk_list(l, n):
    """
    Return a list of chunks
    :param l: List
    :param n: int The number of items per chunk
    :return: List
    """
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


def any_in_list(l1, l2):
    """
    Check if any items in list1 is in list2
    :param l1: list or string
    :param l2: list or string
    :return: bool
    """
    if isinstance(l1, str):
        l1 = l1.split()
    if isinstance(l2, str):
        l2 = l2.split()
    return any(x in l2 for x in l1)


def to_struct(**kwargs):
    """
    Convert kwargs to struct
     a = to_struct(Name='Hello', Value='World' )
     a.Name -> Hello

     :return object:
    """
    return type('', (), kwargs)


def encrypt_string(string):
    """
    Encrypt a string
    """
    return crypt_engine.encrypt(string)


def verify_encrypted_string(string, encrypted_string):
    """
    Verify an encrypted string
    """
    return crypt_engine.verify(string, encrypted_string)


def generate_random_string(length=8):
    """
    Generate a random string
    """
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set * (length - 1), length))


def generate_random_hash(size=32):
    """
    Return a random hash key
    :param size: The max size of the hash
    :return: string
    """
    return os.urandom(size // 2).encode('hex')


def get_pkg_resources_filename(pkg, filename=''):
    """
    Returns a string filepath from a package name/path
    It helps get the full path from a package directory
    :param pkg: str - The dotted path of package dir: portofolio.component, or flask_magic.component.views
    :param filename: str - The file or dir name to use use
    returns str
    """
    return pkg_resources.resource_filename(pkg, filename)


def get_domain_name(url):
    """
    Get the domain name
    :param url:
    :return:
    """
    if not url.startswith('http'):
        url = 'http://' + url
    if not is_url_valid(url):
        raise ValueError("Invalid URL '%s'" % url)
    parse = urlparse(url)
    return parse.netloc


def seconds_to_time(sec):
    """
    Convert seconds into time H:M:S
    """
    return '%02d:%02d' % divmod(sec, 60)


def time_to_seconds(t):
    """
    Convert time H:M:S to seconds
    """
    l = list(map(int, t.split(':')))
    return sum(n * sec for n, sec in zip(l[::-1], (1, 60, 3600)))


def is_port_open(port, host='127.0.0.1'):
    """
    Check if a port is open
    :param port:
    :param host:
    :return bool:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except Exception as e:
        return False


def run(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()[0].strip()


def convert_bytes(bytes):
    """
    Convert bytes into human readable
    """
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    else:
        if bytes >= 1073741824:
            gigabytes = bytes / 1073741824
            size = '%.2fG' % gigabytes
        else:
            if bytes >= 1048576:
                megabytes = bytes / 1048576
                size = '%.2fM' % megabytes
            else:
                if bytes >= 1024:
                    kilobytes = bytes / 1024
                    size = '%.2fK' % kilobytes
                else:
                    size = '%.2fb' % bytes
    return size


def list_chunks(l, n):
    """
    Return a list of chunks
    :param l: List
    :param n: int The number of items per chunk
    :return: List
    """
    if n < 1:
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]


def time_ago(dt):
    """
    Return the current time ago
    """
    now = datetime.datetime.now()
    return humanize.naturaltime(now - dt)


def bg_process(func):
    """
    A multiprocess decorator
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        p = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        p.start()

    return wrapper


def bg_thread(func):
    """
    A threading decorator
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        p = threading.Thread(target=func, args=args, kwargs=kwargs)
        p.start()

    return wrapper


class DotDict(dict):
    __doc__ = "\n    Enable use of object notation for dicts.\n    The __missing__ method allows chaining creation of nested DotDicts:\n    a = DotDict() ; a.foo.bar = 'content'\n    Limitation: Expressing keys as attributes limits keys to valid Python\n    identifiers.\n    "
    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__

    def __setattr__(self, key, value):
        if hasattr(value, 'keys'):
            value = DotDict(value)
        self[key] = value

    def __missing__(self, key):
        self[key] = DotDict()
        return self[key]

    def get(self, keys, default=None):
        """
        To get a value by dot notation
        :param keys: dot notaion string
        :param default:
        :return:
        """
        try:
            d = self
            for k in keys.split('.'):
                if k not in d:
                    d[k] = {}
                d = d[k]

            if isinstance(d, bool):
                return d
            else:
                return d or default
        except (TypeError, KeyError) as e:
            return default


class InspectDecoratorCompatibilityError(Exception):
    pass


class _InspectMethodsDecorators(object):
    __doc__ = '\n    This class attempt to retrieve all the decorators in a method\n    '

    def __init__(self, method):
        self.method = method
        self.decos = []

    def parse(self):
        """
        Return the list of string of all the decorators found
        """
        self._parse(self.method)
        return list(set([deco for deco in self.decos if deco]))

    @classmethod
    def extract_deco(cls, line):
        line = line.strip()
        if line.startswith('@'):
            if '(' in line:
                line = line.split('(')[0].strip()
            return line.strip('@')

    def _parse(self, method):
        argspec = inspect.getargspec(method)
        args = argspec[0]
        if args and args[0] == 'self':
            return argspec
        if hasattr(method, '__func__'):
            method = method.__func__
        if not hasattr(method, '__closure__') or method.__closure__ is None:
            raise InspectDecoratorCompatibilityError
        closure = method.__closure__
        for cell in closure:
            inner_method = cell.cell_contents
            if inner_method is method:
                pass
            else:
                if not inspect.isfunction(inner_method) and not inspect.ismethod(inner_method):
                    pass
                else:
                    src = inspect.getsourcelines(inner_method)[0]
                    self.decos += [self.extract_deco(line) for line in src]
                    self._parse(inner_method)


def get_decorators_list(method):
    """
    Shortcut to InspectMethodsDecorators
    :param method: object
    :return: List
    """
    kls = _InspectMethodsDecorators(method)
    return kls.parse()