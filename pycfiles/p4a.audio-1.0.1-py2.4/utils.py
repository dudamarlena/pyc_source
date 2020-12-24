# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/utils.py
# Compiled at: 2007-11-27 08:43:15
DEFAULT_CHARSET = 'utf-8'

def unicodestr(v, charset=DEFAULT_CHARSET):
    ur"""Return the unicode object representing the value passed in an
    as error-immune manner as possible.

      >>> unicodestr(u'foo')
      u'foo'
      >>> unicodestr('bar')
      u'bar'
      >>> unicodestr('héllo wórld', 'ascii')
      u'h\ufffd\ufffdllo w\ufffd\ufffdrld'

      >>> class Mock(object):
      ...     def __repr__(self): return '<Mock>'
      >>> unicodestr(Mock(), 'ascii')
      u'<Mock>'
    """
    if isinstance(v, unicode):
        return v
    if isinstance(v, str):
        return v.decode(charset, 'replace')
    return unicode(v)