# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\CODE\VScode\workspace\test01\xmind2.0\xxmind\file\xmind-sdk-python-master\xmind\utils.py
# Compiled at: 2018-11-13 07:00:38
"""
    xmind.utils
    ~~~~~~~~~~~

    :mod:``xmind.utils`` provide a handy way for internal used by
    xmind, and excepted that function defined here will be useful to
    others.

    :copyright:
    :license:
"""
__author__ = 'aiqi@xmind.net <Woody Ai>'
import os, time, random, tempfile, zipfile
from hashlib import md5
from functools import wraps
from xml.dom.minidom import parse, parseString
temp_dir = tempfile.mkdtemp

def extract(path):
    return zipfile.ZipFile(path, 'r')


def compress(path):
    return zipfile.ZipFile(path, 'w')


join_path = os.path.join
split_ext = os.path.splitext

def get_abs_path(path):
    """
        Return the absolute path of a file

        If path contains a start point (eg Unix '/') then use the specified start point
        instead of the current working directory. The starting point of the file
        path is allowed to begin with a tilde "~", which will be replaced with the user's
        home directory.
    """
    fp, fn = os.path.split(path)
    if not fp:
        fp = os.getcwd()
    fp = os.path.abspath(os.path.expanduser(fp))
    return join_path(fp, fn)


def get_current_time():
    """
    Get the current time in milliseconds
    """
    return long(round(time.time() * 1000))


def readable_time(timestamp):
    """
    Convert timestamp to human-readable time format
    """
    timestampe_in_seconds = float(timestamp) / 1000
    return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(timestampe_in_seconds))


parse_dom = parse
parse_dom_string = parseString

def generate_id():
    """
    Generate unique 26-digit random string
    """
    timestamp = md5(str(get_current_time())).hexdigest()
    lotter = md5(str(random.random())).hexdigest()
    id = timestamp[19:] + lotter[:13]
    return id.decode('utf8')


def prevent(func):
    """
        Decorate func with this to prevent raising an Exception when
        an error is encountered
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return

    return wrapper


def check(attr):

    def decorator(method):
        """
            Decorate method with this to check whether the object
            has an attribute with the given name.
        """

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, attr):
                return method(self, *args, **kwargs)
            else:
                return

        return wrapper

    return decorator


def main():
    pass


if __name__ == '__main__':
    main()