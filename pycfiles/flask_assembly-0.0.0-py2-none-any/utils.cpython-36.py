# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/flasik/utils.py
# Compiled at: 2019-09-07 12:28:17
# Size of source mod 2**32: 7831 bytes
"""
utils.py

This module contains some common functions, and also exposes under the `utils`
namespace some 3rd party functions. ie: 
    utils.slugify 
    utils.dasherize
    
others:
    utils.is_email_valid
    utils.md5(string)

"""
from __future__ import division
import os, re, inspect, time, datetime, arrow, string, random, socket, itsdangerous, humanize, pkg_resources, urllib, hashlib, json, uuid
from six import string_types
from slugify import slugify
from werkzeug.utils import import_string
from distutils.dir_util import copy_tree as copy_dir, remove_tree as remove_dir, mkpath as make_dirs
from distutils.file_util import copy_file, move_file
from inflection import dasherize, underscore, camelize, pluralize, singularize, titleize
from six.moves.urllib.parse import urlparse, urlencode, unquote_plus as urllib_unquote_plus
__all__ = [
 'is_email_valid',
 'is_password_valid',
 'is_username_valid',
 'is_url_valid',
 'urldecode',
 'urlencode',
 'md5',
 'guid',
 'slugify',
 'chunk_list',
 'in_any_list',
 'dict_dot',
 'list_replace',
 'dict_replace',
 'to_json',
 'dasherize',
 'undescore',
 'camelize',
 'plurialize',
 'singularize',
 'titleize']

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


def is_username_valid(username):
    """
    Check if a valid username.
    valid:
        oracle
        bill-gates
        steve.jobs
        micro_soft
    not valid
        Bill Gates - no space allowed
        me@yo.com - @ is not a valid character
    :param username: string
    :return:
    """
    pattern = re.compile('^[a-zA-Z0-9_.-]+$')
    return bool(pattern.match(username))


def is_url_valid(url):
    """
    Check if url is valid
    """
    pattern = re.compile('^(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+(?:[A-Z]{2,6}\\.?|[A-Z0-9-]{2,}\\.?)|\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})(?::\\d+)?(?:/?|[/?]\\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))


def urldecode(s):
    return urllib_unquote_plus(s)


def md5(value):
    """
    Create MD5
    :param value:
    :return:
    """
    m = hashlib.md5()
    m.update(value)
    return str(m.hexdigest())


def guid():
    """
    Creates and returns a UUID 4 hex value
    :return: string
    """
    return uuid.uuid4().hex


def chunk_list(items, size):
    """
    Return a list of chunks
    :param items: List
    :param size: int The number of items per chunk
    :return: List
    """
    size = max(1, size)
    return [items[i:i + size] for i in range(0, len(items), size)]


def in_any_list(items1, items2):
    """
    Check if any items are in list2
    :param items1: list
    :param items2: list
    :return:
    """
    return any(i in items2 for i in items1)


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


class dict_dot(dict):
    __doc__ = '\n    A dict extension that allows dot notation to access the data.\n    ie: dict.get(\'key.key2.0.keyx\')\n    my_dict = {...}\n    d = dict_dot(my_dict)\n    d.get("key1")\n    d.get("key1.key2")\n    d.get("key3.key4.0.keyX")\n\n    Still have the ability to access it as a normal dict\n    d[key1][key2]\n    '

    def get(self, key, default=None):
        """
        Access data via
        :param key:
        :param default: the default value
        :return:
        """
        try:
            val = self
            if '.' not in key:
                return self[key]
            for k in key.split('.'):
                if k.isdigit():
                    k = int(k)
                val = val[k]

            return val
        except (TypeError, KeyError, IndexError) as e:
            return default


def list_replace(subject_list, replacement, string):
    """
    To replace a list of items by a single replacement
    :param subject_list: list
    :param replacement: string
    :param string: string
    :return: string
    """
    for s in subject_list:
        string = string.replace(s, replacement)

    return string


def dict_replace(subject_dict, string):
    """
    Replace a dict map, key to its value in the stirng
    :param subject_dict: dict
    :param string: string
    :return: string
    """
    for i, j in subject_dict.items():
        string = string.replace(i, j)

    return string


def to_json(d):
    """
    Convert data to json. It formats datetime/arrow time
    :param d: dict or list
    :return: json data
    """
    return json.dumps(d, cls=_FlasikJSONEncoder)


class _FlasikJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, arrow.Arrow):
            return obj.for_json()
        else:
            if isinstance(obj, datetime.datetime):
                return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
            if isinstance(obj, datetime.date):
                return obj.strftime('%Y-%m-%d')
            return json.JSONEncoder.default(self, obj)


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
        if args:
            if args[0] == 'self':
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
                if not inspect.isfunction(inner_method):
                    if not inspect.ismethod(inner_method):
                        continue
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