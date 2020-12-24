# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/scott/.virtualenvs/carinata/lib/python2.7/site-packages/carinata/utils.py
# Compiled at: 2013-05-19 07:06:28
__doc__ = 'String utilities for creating unittest files from spec files'
import hashlib, os, sys, uuid
VALID_IDENTIFIER = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ12345678990_'

class FileHashMatch(Exception):
    """The persisted file has a hash, and it matched the current file hash"""
    fmt = 'File {0} matched old file with hash {1}'

    def __init__(self, filename, hash):
        self.filename = filename
        self.hash = hash
        self.message = self.fmt.format(filename, hash)


def _camel_safe(name):
    """Remove all non-identifier chars and underscores from name"""
    return identifier_safe(name).replace('_', '')


def identifier_safe(name):
    """Remove all non-identifier chars from name"""
    return ('').join(char for char in name if char in VALID_IDENTIFIER)


def camelify(words):
    """Return a camel-cased version of words"""
    return ('').join(_camel_safe(w) for w in words.title() if not w.isspace())


def snakify(words):
    """Return a snake-cased version of words"""
    return ('_').join(identifier_safe(w) for w in words.lower().split())


def create_module_from_file(filepath):
    """Execute string as if it were a module, and return that module"""
    name = os.path.splitext(os.path.basename(filepath))[0]
    directory = os.path.dirname(filepath)
    if directory not in sys.path:
        sys.path.insert(0, directory)
    return __import__(name)


def uuid_hex(length=6):
    return '_x' + uuid.uuid4().hex[:length]


def get_hash_from_contents(contents):
    return hashlib.sha1(contents).hexdigest()


def get_hash_from_filename(filename, block=4096):
    sha1 = hashlib.sha1()
    with open(filename) as (f):
        while True:
            data = f.read(block)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()


def get_hash_from_first_line(filename):
    with open(filename, 'r') as (f):
        hash_line = f.readline()
    try:
        return hash_line.split(':')[1].strip()
    except IndexError:
        return ''


def check_file_hash(input_filename, output_filename):
    current_hash = get_hash_from_filename(input_filename)
    if os.path.exists(output_filename):
        old_hash = get_hash_from_first_line(output_filename)
        if current_hash == old_hash:
            raise FileHashMatch(output_filename, current_hash)