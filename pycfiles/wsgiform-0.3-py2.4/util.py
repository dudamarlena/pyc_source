# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiform\util.py
# Compiled at: 2006-12-06 22:59:37
"""Utilities for server-side form processing."""
import cgi, re, string
from StringIO import StringIO
from xml.sax import saxutils
__all__ = [
 'hyperescape', 'escape', 'sterilize', 'escapeform', 'hyperform', 'sterileform']
_trans = string.maketrans('', '')

def getinput(environ):
    """Non-destructively retrieves wsgi.input value."""
    wsginput = environ['wsgi.input']
    if hasattr(wsginput, 'getvalue'):
        qs = wsginput.getvalue()
    else:
        clength = int(environ['CONTENT_LENGTH'])
        qs = wsginput.read(clength)
        environ['wsgi.input'] = StringIO(qs)
    return qs


def formparse(environ, strict=False):
    """Stores data from form submissions in a dictionary.

    @param environ Environment dictionary
    @param strict Stops on errors (default: False)
    """
    qdict = cgi.parse(StringIO(getinput(environ)), environ, strict, strict)
    for (key, value) in qdict.iteritems():
        if len(value) == 1:
            qdict[key] = value[0]

    return qdict


def _runfunc(qdict, func):
    """Runs a function on a dictionary.

    @param qdict Dictionary
    @param func Function
    """
    for (key, value) in qdict.iteritems():
        if isinstance(value, basestring):
            qdict[key] = func(value)
        elif isinstance(value, list):
            for (num, item) in enumerate(value):
                if isinstance(item, basestring):
                    value[num] = func(item)

    return qdict


def escape(data):
    """Escapes &, <, >, ", and ' with HTML entities.

    @param data Text data
    """
    return saxutils.escape(data, {'"': '&quot;', "'": '&#39;'})


def escapeform(environ, strict=False):
    """Escapes common XML/HTML entities in form data.

    @param environ Environment dictionary
    @param strict Stops on errors (default: False)
    """
    return _runfunc(formparse(environ, strict), escape)


def hyperescape(data):
    """Escapes punctuation with HTML entities except ., -, and _.

    @param data Text data
    """
    data = re.sub('&(?!#\\d\\d;)', '&#38;', data)
    data = re.sub('(?<!&#\\d\\d);', '&#59;', data)
    data = re.sub('(?<!&)#(?!\\d\\d;)', '&#35;', data)
    for char in '<>"\'()!${}*+,%/:=?@[\\]^`|~':
        data = data.replace(char, '&#%d;' % ord(char))

    return data


def hyperform(environ, strict=False):
    """Hyper-escapes all XML/HTML entitites in form data.

    @param environ Environment dictionary
    @param strict Stops on errors (default: False)
    """
    return _runfunc(formparse(environ, strict), hyperescape)


def sterileform(environ, strict=False):
    """Removes all form data characters except alphanumerics, ., -, and _.

    @param environ Environment dictionary
    @param strict Stops on errors (default: False)
    """
    return _runfunc(formparse(environ, strict), sterilize)


def sterilize(data):
    """Removes all ASCII characters except alphanumerics, ., -, and _.

    @param data Text data
    """
    return data.translate(_trans, '&#;<>"\'()!${}*+,%/:=?@[\\]^`|~')