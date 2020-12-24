# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/t/work/cihai/cihai/cihai/_compat.py
# Compiled at: 2019-08-17 10:47:47
# Size of source mod 2**32: 1262 bytes
import sys
PY2 = sys.version_info[0] == 2
if PY2:
    unichr = unichr
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
    from urllib import urlretrieve
    from cStringIO import StringIO as BytesIO
    from StringIO import StringIO
    import cPickle as pickle, urlparse, collections as collections_abc

    def console_to_str(s):
        return s.decode('utf_8')


    exec('def reraise(tp, value, tb=None):\n raise tp, value, tb')
else:
    unichr = chr
    text_type = str
    string_types = (str,)
    integer_types = (int,)
    from io import StringIO, BytesIO
    import urllib.parse as urllib
    import urllib.parse as urlparse
    from urllib.request import urlretrieve
    import collections.abc as collections_abc
    console_encoding = sys.__stdout__.encoding

    def console_to_str(s):
        """ From pypa/pip project, pip.backwardwardcompat. License MIT. """
        try:
            return s.decode(console_encoding)
        except UnicodeDecodeError:
            return s.decode('utf_8')


    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value