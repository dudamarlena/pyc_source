# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htmllist/utills.py
# Compiled at: 2010-10-16 07:02:00
"""
Utilities Module
"""
import re, itertools
from htmlentitydefs import entitydefs
from string import maketrans
from urllib2 import urlopen, Request, HTTPError

def iter2tuple(func):
    """ Simple decorator to convert iterator to a tuple """

    def _iter2tuple(*args, **kw):
        return tuple(func(*args, **kw))

    return _iter2tuple


def not_empty_iter(func):
    """ Decorator over a function that returns an iterator. If the returned
        iterator is empty, it will return None. So the user can (must) check if the
        iterator is not None before using it.
        """

    def _not_empty_iter(*args, **kw):
        itr = func(*args, **kw)
        try:
            first = itr.next()
        except StopIteration:
            return

        return itertools.chain([first], itr)
        return

    return _not_empty_iter


_re_unquote = re.compile('&(#?)(.+?);')
entitydefs['nbsp'] = ' '

def unquote_html(string):
    """ Convert an HTML quoted string into normal string (ISO-8859-1).
        Works with &#XX; and with &nbsp; &gt; etc.
        From: http://groups.google.com/group/comp.lang.python/browse_thread/thread/7f96723282376f8c/
        """

    def _convert_entity(m):
        if m.group(1) == '#':
            try:
                return chr(int(m.group(2)))
            except ValueError:
                return '&#%s;' % m.group(2)

        try:
            return entitydefs[m.group(2)]
        except KeyError:
            return '&%s;' % m.group(2)

    if not string:
        return string
    return _re_unquote.sub(_convert_entity, string)


_re_quote = re.compile('(["<>])|(&)[^\\s;]*(;)?')
_convertion_table = {'"': '&quot;', 
   '<': '&lt;', 
   '>': '&gt;', 
   '&': '&amp;'}

def quote_html(string):
    """ Quote the <, >, " symbols and the & symbol if it is not part of &xxx; """

    def _convert_entity(m):
        if m.group(1):
            return _convertion_table[m.group(1)]
        if m.group(2) and not m.group(3):
            return _convertion_table[m.group(2)]

    if not string:
        return string
    return _re_quote.sub(_convert_entity, string)


_ptrn_script = '<script\n\t(\n\t\t# [^>]*/> | # Links that closes in the start tag (<script .... />)\n\t\t[^>]*> .*? </script> # Regular <script>...</script>\n\t)\n'
_re_script = re.compile(_ptrn_script, re.DOTALL | re.VERBOSE | re.IGNORECASE)

def strip_scripts(data):
    """ Removes <script> tags from a string """
    return _re_script.sub(' ', data)


_re_tags = re.compile('\\s*(<.*?>\\s*)+', re.DOTALL)

def strip_tags(data, replacement=' '):
    """ Removes any tag from a string """
    return _re_tags.sub(replacement, data)


def url_open(url, user_agent=None, err=None):
    """ Open a URL with an optional user agent.
        url can be a string or a Request instance

        If err is a list object, in case of URL-Error it will append to this list
        the error code, error message, and URL

        Return the pages text.
        """
    text = ''
    try:
        if not isinstance(url, Request):
            req = Request(url)
        else:
            req = url
        if user_agent:
            req.add_header('user-agent', user_agent)
        page = urlopen(req)
        text = page.read()
        page.close()
    except HTTPError, e:
        if isinstance(err, list):
            err.append(e.code)
            err.append(e.msg)
            err.append(e.url)
        print 'Cannot open:', e.url, e.msg, e.code
    except:
        print 'Error opening:', url

    return text


if __name__ == '__main__':
    err_lst = []
    url_open('http://pyhtmllist.sourceforge.net/foo.bar', err=err_lst)
    assert err_lst