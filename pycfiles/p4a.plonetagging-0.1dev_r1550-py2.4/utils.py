# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/p4a/plonetagging/utils.py
# Compiled at: 2007-10-12 18:11:48


def escape(v):
    ur"""Take the string, list, tuple, or set and return one unicode string
    that connects all of the values by spaces with values that already
    contained spaces in double quotes.

      >>> escape([u'abc', u'def'])
      u'abc def'

      >>> escape([u'test with spaces', u'foo'])
      u'"test with spaces" foo'

      >>> escape(u'foo bar')
      u'"foo bar"'

      >>> escape('nonascii_köln')
      u'nonascii_k\xf6ln'

    """
    if not isinstance(v, (tuple, list, set)):
        v = [
         v]
    result = []
    for x in v:
        if not isinstance(x, unicode):
            x = str(x).decode('utf-8')
        if x.find(' ') > -1:
            x = '"%s"' % x
        result.append(x)

    return (' ').join(result)


def unescape(v):
    """Take the unicode string and return a list containing the broken
    up values from the unicode string (separated by spaces).

      >>> unescape(u'foo bar')
      [u'foo', u'bar']

      >>> unescape(u'foo "testing spaces" bar')
      [u'foo', u'testing spaces', u'bar']

      >>> unescape(u'"testing spaces" bar')
      [u'testing spaces', u'bar']

    """
    result = []
    last = ''
    inquote = False
    for x in v:
        if x == '"':
            if not inquote:
                inquote = True
            elif inquote:
                inquote = False
        elif x == ' ' and not inquote:
            last = last.strip()
            if last:
                result.append(last)
            last = ''
        else:
            last += x

    last = last.strip()
    if last:
        result.append(last)
    return result