# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/urilib/tools.py
# Compiled at: 2011-08-25 23:30:03
import urilib.regex, re

def is_valid_scheme(scheme):
    """ Verify that the scheme meets the spec from RFC 3986 """
    scheme_re = re.compile('^%s$' % urilib.regex.scheme, re.I | re.U)
    return scheme_re.match(scheme) is not None


def is_valid_fragment(fragment):
    """ Verify that the fragment meets the spec from RFC 3986 """
    fragment_re = re.compile('^%s$' % urilib.regex.fragment, re.I | re.U)
    return fragment_re.match(fragment) is not None


def is_valid_query(query):
    """ Verify that the query meets the spec from RFC 3986 """
    query_re = re.compile('^%s$' % urilib.regex.query, re.I | re.U)
    return query_re.match(query) is not None


def is_valid_userinfo(userinfo):
    """ Verify that the userinfo meets the spec from RFC 3986 """
    userinfo_re = re.compile('^%s$' % urilib.regex.userinfo, re.I | re.U)
    return userinfo_re.match(userinfo) is not None