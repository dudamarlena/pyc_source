# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gabriel.falcao/Projetos/bolacha/bolacha/multipart.py
# Compiled at: 2010-12-06 07:18:56
import types
from uuid import uuid4
from urllib import quote_plus, urlencode
from glob import glob
from os.path import basename
from mimetypes import guess_type
BOUNDARY = uuid4().hex

def is_file(obj):
    return hasattr(obj, 'read') and callable(obj.read)


def to_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """ took from django smart_str """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                return (' ').join([ smart_str(arg, encoding, strings_only, errors) for arg in s
                                  ])
            return unicode(s).encode(encoding, errors)

    else:
        if isinstance(s, unicode):
            return s.encode(encoding, errors)
        else:
            if s and encoding != 'utf-8':
                return s.decode('utf-8', errors).encode(encoding, errors)
            return s


def expand_items(dictionary):
    """
    Given a dict like {'key': ('value1', 'value2')} returns
    a list like [('key','value1'), ('key', 'value2')]
    """
    items = []
    for (key, value) in dictionary.items():
        if isinstance(value, (list, tuple)):
            items.extend([ (key, item) for item in value ])
        else:
            items.append((key, value))

    return items


def encode_multipart(boundary, data):
    lines = []
    for (key, value) in expand_items(data):
        if is_file(value):
            lines.extend(encode_file(boundary, key, value))
        elif is_file(value):
            lines.extend(encode_file(boundary, key, value))
        else:
            lines.extend([
             '--' + boundary,
             'Content-Disposition: form-data; name="%s"' % to_str(key),
             '',
             to_str(value)])

    lines.extend([
     '--' + boundary + '--',
     ''])
    return ('\r\n').join(lines)


def guess_mime(path):
    (mime, x) = guess_type(path)
    return mime or 'application/octet-stream'


def encode_file(boundary, key, file):
    return [
     '--' + boundary,
     'Content-Disposition: form-data; name="%s"; filename="%s"' % (
      to_str(key), to_str(basename(file.name))),
     'Content-Type: %s' % guess_mime(file.name),
     '',
     to_str(file.read())]